from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.preprocessing import normalize
import os
import copy
from nltk import download
# nltk stopwords are used, because CountVectorizer's stop words list is controversal. Nltk's list is quite small
# and thus should be more robust. Source https://www.aclweb.org/anthology/W18-2502
from nltk.corpus import stopwords
# scipy's implementation of eigen vector calculation is more robust
# and applies different kinds of optimization for better numerical stability
from scipy.linalg import eigh

affinity_threshold = 0.1
dumping_factor = 0.85
#download('stopwords')


class InputDocument:

    def __init__(self, docid, content, query_similarity):
        self.docid = docid
        self.content = content
        self.query_similarity = query_similarity


class RankedDocument:

    def __init__(self, docid, content, score, query_similarity, index):
        self.docid = docid
        self.content = content
        self.score = score
        self.info_rich = score
        self.query_similarity = query_similarity
        self.index = index


# affinity measure between documents, mathematically it is a projection of vector2 on vector1
def affinity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    vector1_norm = np.linalg.norm(vector1)
    if vector1_norm > 0:
        score = dot_product/vector1_norm
        return score
    return 0


def convert_documents_to_vectors(collection):
    stop_words = stopwords.words('english')
    # stop words are removed from vector space since they add no value to documents similarity
    count_vectorizer = CountVectorizer(stop_words=stop_words)
    document_vectors = count_vectorizer.fit_transform(collection)
    document_vectors = document_vectors.toarray()
    return document_vectors


def get_affinity_matrix(collection):
    document_vectors = convert_documents_to_vectors(collection)
    collection_size = len(document_vectors)
    affinity_matrix = np.zeros((collection_size, collection_size))
    # TODO: try to improve this code
    for i, document_0 in enumerate(document_vectors):
        for j, document_1 in enumerate(document_vectors):
            # from the paper it is unclear if they keep zero diagonal or not. I'm inclined to think that adjacency/affinity
            # matrix should have zero diagonal, because we do not need the information about the similarity of a document to itself
            if i != j:
                affinity_matrix[i, j] = affinity(document_0, document_1)

    # normalize by division at max item to make matrix items belong to 0..1 interval
    # but preserve the relation between all the matrix items
    # optional, done for convenience of defining the threshold and its more intuitive understanding
    return affinity_matrix /np.amax(affinity_matrix)


def apply_threshold(affinity):
    return affinity if affinity >= affinity_threshold else 0


# TODO: for the final implementation get rid of this method and put the logic to get_affinity_matrix
# Now it is still useful for debuging
def get_adjacency_matrix(affinity_matrix):
    # the best criteria I came up with so far
    median = np.median(affinity_matrix[np.where(affinity_matrix > 0)])
    maximum = np.amax(affinity_matrix)
    print("Affinity matrix maximum {}, median (excluding zero values) {}".format(maximum, median))
    non_zero_items = np.size(affinity_matrix[np.where(affinity_matrix > affinity_threshold)])
    size = np.shape(affinity_matrix)
    print("Number of edges in affinity graph of {}. Graph number of nodes {}".format(non_zero_items, size[0]))

    # i think there is a better way to do it, but I haven't found it
    adjacency_matrix = np.zeros(size)

    for i in range(0, size[0]):
        for j in range(0, size[1]):
            adjacency_matrix[i, j] = apply_threshold(affinity_matrix[i, j])

    if np.count_nonzero(adjacency_matrix) == 0:
        print("Warning: affinity graph has no edges")

    # we will use normalized matrix, this way of normalization will work if there are zero only rows
    return normalize(adjacency_matrix, axis=1, norm='l1')


def get_transition_matrix(adjacency_matrix, dumping_factor):
    n, _ = adjacency_matrix.shape
    transition_matrix = dumping_factor*adjacency_matrix.transpose() + ((1-dumping_factor)/n) * np.ones(n)/n
    return transition_matrix


def get_document_rank(transition_matrix):
    eigen_values, eigen_vectors = eigh(transition_matrix)
    # principal eigen vector is the one which corresponds to the largest eigen value
    principal_eigen_vector = eigen_vectors[:, eigen_values.argmax()]
    # normalize
    principal_eigen_vector /= principal_eigen_vector.sum()
    return principal_eigen_vector


def diversity_penalty(documents, adjacency_matrix):
    diversity_penalized_ranking = []
    remaining_documents = copy.deepcopy(documents)

    while len(remaining_documents) > 0:
        remaining_documents.sort(key=lambda x: x.score, reverse=True)
        top_document = remaining_documents.pop(0)
        diversity_penalized_ranking.append(top_document)
        for document in remaining_documents:
            document.score = document.score - adjacency_matrix[document.index, top_document.index]*top_document.info_rich

    # shift scores to remove negative values so that we could apply log normalization
    # shifting does not affect ranking and difference between scores
    min_score = diversity_penalized_ranking[-1].score
    if min_score < 0:
        for document in diversity_penalized_ranking:
            document.score -= min_score

    return diversity_penalized_ranking


# documents is a list of InputDocument class instances
def get_affinity_ranking(documents):
    documents_content = list(map(lambda x: x.content, documents))
    affinity_matrix = get_affinity_matrix(documents_content)
    adjacency_matrix = get_adjacency_matrix(affinity_matrix)
    transition_matrix = get_transition_matrix(adjacency_matrix, dumping_factor)
    document_rank = get_document_rank(transition_matrix)

    ranked_documents = []
    for index, document in enumerate(documents):
        score = document_rank[index]
        ranked_documents.append(RankedDocument(document.docid, document.content, score, document.query_similarity, index))

    ranked_documents.sort(key=lambda x: x.score, reverse=True)

    diversity_penalized_ranking = diversity_penalty(ranked_documents, adjacency_matrix)
    return diversity_penalized_ranking


# TODO: mote to test folder
def get_documents():
    docs = []
    for the_file in os.listdir("docs"):
        if the_file.endswith(".txt"):
            file = open(os.path.join("docs", the_file), mode='r')
            docs.append(file.read().strip())
            file.close()

    return docs


def main():
    # TODO: mote to tests
    docs = get_documents()

    affinity_matrix = get_affinity_matrix(docs)
    print("Affinity")
    print(affinity_matrix)
    adjacency_matrix = get_adjacency_matrix(affinity_matrix)
    print("Adjacency")
    print(adjacency_matrix)
    transition_matrix = get_transition_matrix(adjacency_matrix, dumping_factor)
    print("Transition")
    print(transition_matrix)
    document_rank = get_document_rank(transition_matrix)
    print("Rank")
    print(document_rank)

    ranked_documents = []
    for index, content in enumerate(docs):
        score = document_rank[index]
        ranked_documents.append(RankedDocument(index, content, score, score, index))

    ranked_documents.sort(key=lambda x: x.score, reverse=True)

    diversity_penalized_ranking = diversity_penalty(ranked_documents, adjacency_matrix)

    print("stop")



if __name__ == '__main__':
    main()

