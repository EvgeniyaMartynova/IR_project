from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def getSimilarityMatrix(docs):
    docs_name = []
    # doc_id = 0
    for i in range(1,len(docs)+1):
        docs_name.append("DOC %d" % i )

    # vectorizer=CountVectorizer(stop_words='english')
    # vectorizer=CountVectorizer()
    vectorizer = TfidfVectorizer()
    sparse_matrix = vectorizer.fit_transform(docs)
    doc_term_matrix = sparse_matrix.todense()

    df = pd.DataFrame(doc_term_matrix, columns=vectorizer.get_feature_names(), index=docs_name)
    return cosine_similarity(df, df)


def main():
    doc_trump = "Mr. Trump became president after winning the political election. Though he lost the support of some republican friends, Trump is friends with President Putin"
    doc_election = "President Trump says Putin had no political interference is the election outcome. He says it was a witchhunt by political parties. He claimed President Putin is a friend who had nothing to do with the election"
    doc_putin = "Post elections, Vladimir Putin became President of Russia. President Putin had served as the Prime Minister earlier in his political career"
    documents = [doc_trump, doc_election, doc_putin]
    result = getSimilarityMatrix(documents)
    print(result)


if __name__ == '__main__':
    main()
