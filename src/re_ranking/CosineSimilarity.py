from sklearn.feature_extraction.text import TfidfVectorizer
import math


def cos_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1]))
    if not magnitude:
        return 0
    return dot_product/magnitude


def getSimilarityMatrix(docs):
    tfidf_vectorizer = TfidfVectorizer()
    vectorized_matrix = tfidf_vectorizer.fit_transform(docs)
    result_matrix = []
    for count_0, doc_0 in enumerate(vectorized_matrix.toarray()):
        for count_1, doc_1 in enumerate(vectorized_matrix.toarray()):
            result_matrix.append((cos_similarity(doc_0, doc_1), count_0, count_1))
    return result_matrix



def main():
    doc_trump = "Mr. Trump became president after winning the political election. Though he lost the support of some republican friends, Trump is friends with President Putin"
    doc_election = "President Trump says Putin had no political interference is the election outcome. He says it was a witchhunt by political parties. He claimed President Putin is a friend who had nothing to do with the election"
    doc_putin = "Post elections, Vladimir Putin became President of Russia. President Putin had served as the Prime Minister earlier in his political career"
    documents = [doc_trump, doc_election, doc_putin]
    result=getSimilarityMatrix(documents)
    print(result)


if __name__ == '__main__':
    main()

