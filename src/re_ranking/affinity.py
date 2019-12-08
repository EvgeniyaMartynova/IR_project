from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.preprocessing import normalize
import os
import copy

# the way I see it now is the it's an arbitrary model parameter
# probably it will need tuning
affinity_threshold = 10
dumping_factor = 0.85


class RankedDocument:

    def __init__(self, content, score, index):
        self.content = content
        self.score = score
        self.info_rich = score
        self.index = index


# affinity measure between documents, mathematically it is a projection of vector2 on vector1
def affinity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    vector1_norm = np.linalg.norm(vector1)
    if vector1_norm > 0:
        score = dot_product/vector1_norm
        return score
    return 0


def get_affinity_matrix(collection):
    collection_size = len(collection)
    count_vectorizer = CountVectorizer()
    document_vectors = count_vectorizer.fit_transform(collection)
    document_vectors = document_vectors.toarray()
    affinity_matrix = np.zeros((collection_size, collection_size))
    # TODO: try to improve this code
    for i, document_0 in enumerate(document_vectors):
        for j, document_1 in enumerate(document_vectors):
            # from the paper it is unclear if they keep zero diagonal or not. I'm inclined to think that adjacency/affinity
            # matrix should have zero diagonal, because we do not need the information about the similarity of a document to itself
            if i != j:
                affinity_matrix[i, j] = affinity(document_0, document_1)
    return affinity_matrix


def apply_threshold(affinity):
    return affinity if affinity >= affinity_threshold else 0


# think about more efficient way to implement it and also how to pass "threshold" to apply_threshold as a parameter
def get_adjacency_matrix(affinity_matrix):
    adjacency_matrix = np.vectorize(apply_threshold)(affinity_matrix)
    # we will use normalized matrix, this way of normalization will work if there are zero only rows
    return normalize(adjacency_matrix, axis=1, norm='l1')


def get_transition_matrix(adjacency_matrix, dumping_factor):
    n, _ = adjacency_matrix.shape
    transition_matrix = dumping_factor*adjacency_matrix.transpose() + ((1-dumping_factor)/n) * np.ones(n)/n
    return transition_matrix


def get_document_rank(transition_matrix):
    eigen_values, eigen_vectors = np.linalg.eig(transition_matrix)
    # principal eigen vector is the one which corresponds to the largest eigen value
    principal_eigen_vector = eigen_vectors[:, eigen_values.argmax()]
    # normalize
    principal_eigen_vector /= principal_eigen_vector.sum()
    return principal_eigen_vector


def get_documents():
    docs = []
    for the_file in os.listdir("docs"):
        if the_file.endswith(".txt"):
            file = open(os.path.join("docs", the_file), mode='r')
            docs.append(file.read().strip())
            file.close()

    return docs


def diversity_penalty(documents, adjacency_matrix):
    diversity_penalized_ranking = []
    remaining_documents = copy.deepcopy(documents)

    while len(remaining_documents) > 0:
        remaining_documents.sort(key=lambda x: x.score, reverse=True)
        top_document = remaining_documents.pop(0)
        diversity_penalized_ranking.append(top_document)
        top_document_index = top_document.index
        top_document_info_rich = top_document.info_rich
        for document in remaining_documents:
            document_index = document.index
            document.score = document.score - adjacency_matrix[document_index, top_document_index]*top_document_info_rich

    return diversity_penalized_ranking


def main():
    docs = get_documents()

    doc_trump = "Mr. Trump became president after winning the political election. Though he lost the support of some republican friends, Trump is friends with President Putin"
    doc_election = "President Trump says Putin had no political interference is the election outcome. He says it was a witchhunt by political parties. He claimed President Putin is a friend who had nothing to do with the election"
    doc_putin = "Post elections, Vladimir Putin became President of Russia. President Putin had served as the Prime Minister earlier in his political career"
    documents = [doc_trump, doc_election, doc_putin]
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
        ranked_documents.append(RankedDocument(content, score, index))

    ranked_documents.sort(key=lambda x: x.score, reverse=True)

    diversity_penalized_ranking = diversity_penalty(ranked_documents, adjacency_matrix)



if __name__ == '__main__':
    main()

