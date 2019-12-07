from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# the way I see it now is the it's an arbitrary model parameter
# probably it will need tuning
affinity_threshold = 2.5

# affinity measure between documents, mathematically it is a projection of vector2 on vector1
def affinity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    vector1_norm = np.linalg.norm(vector1)
    if vector1_norm > 0:
        return dot_product/vector1_norm
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
            affinity_matrix[i, j] = affinity(document_0, document_1)
    return affinity_matrix


def apply_threshold(affinity):
    return affinity if affinity >= affinity_threshold else 0


# think about more efficient way to implement it and also how to pass "threshold" to apply_threshold as a parameter
def get_adjacency_matrix(affinity_matrix):
    return np.vectorize(apply_threshold)(affinity_matrix)


def main():
    doc_trump = "Mr. Trump became president after winning the political election. Though he lost the support of some republican friends, Trump is friends with President Putin"
    doc_election = "President Trump says Putin had no political interference is the election outcome. He says it was a witchhunt by political parties. He claimed President Putin is a friend who had nothing to do with the election"
    doc_putin = "Post elections, Vladimir Putin became President of Russia. President Putin had served as the Prime Minister earlier in his political career"
    documents = [doc_trump, doc_election, doc_putin]
    affinity_matrix = get_affinity_matrix(documents)
    print(affinity_matrix)
    adjacency_matrix = get_adjacency_matrix(affinity_matrix)
    print(adjacency_matrix)


if __name__ == '__main__':
    main()

