
from pyserini.search import pysearch
import affinity_ranking as ar
import matplotlib.pyplot as plt
import numpy as np

# tunable coefficients for scores linear combination
# query similarity measure score
alpha = 0.75
# affinity ranking score
beta = 1 - alpha


class ReRankedDocument:

    def __init__(self, docid, content, score):
        self.docid = docid
        self.content = content
        self.score = score


def plot_scores(hits, ar_documents, re_ranked_documents):
    max_similarity_score = hits[0].score
    max_affinity_score = ar_documents[0].score

    original_scores = list(map(lambda x: x.score / max_similarity_score, hits))
    affinity_scores = list(map(lambda x: x.score / max_affinity_score, ar_documents))
    re_ranked_scores = list(map(lambda x: x.score, re_ranked_documents))
    t = np.arange(0, len(hits), 1)

    plt.figure()
    plt.subplot(311)
    plt.plot(t, original_scores)
    plt.suptitle('Original')

    plt.subplot(312)
    plt.plot(t, affinity_scores)
    plt.suptitle('Affinity')

    plt.subplot(313)
    plt.plot(t, re_ranked_scores)
    plt.suptitle('Re-ranked')
    plt.show()


'''
   results : list of io.anserini.search.SimpleSearcher$Result
   Result class properties
   - docid
   - score - in this case will be standard BM25 score
   - content - document text
'''
def extract_docs_for_reranking(query, index_path, K):
    searcher = pysearch.SimpleSearcher(index_path)
    hits = searcher.search(query, K)
    return hits


def re_rank_docs(hits):
    docs_to_re_rank = list(map(lambda x: ar.InputDocument(x.docid, x.content, x.score), hits))
    ar_documents = ar.get_affinity_ranking(docs_to_re_rank)

    max_similarity_score = hits[0].score
    max_affinity_score = ar_documents[0].score

    re_ranked_documents = []
    for document in ar_documents:
        normalized_similarity_score = document.query_similarity / max_similarity_score
        # for some reason in paper they use average log normalization of affinity ranking.
        # I tried to apply it after shifting the values to be > 0
        # But it does make sense, because after normalization with log(max_affinity_score)
        # the shape of the curve it the same as with average normalization
        normalized_affinity_score = document.score / max_affinity_score
        final_score = alpha*normalized_similarity_score + beta*normalized_affinity_score
        re_ranked_document = ReRankedDocument(document.docid, document.content, final_score)
        re_ranked_documents.append(re_ranked_document)

    re_ranked_documents.sort(key=lambda x: x.score, reverse=True)
    # to compare the scores variation. I would include it into appendix to justify the normalization choice
    # and also to point out how the shape of affinity ranks curve affects the results
    # (this is the disadvantage in my opinion, see "images/Affinity ranking")
    plot_scores(hits, ar_documents, re_ranked_documents)

    return re_ranked_documents


def main():
    # Depends on local environment
    # original search results
    hits = extract_docs_for_reranking("Blue Creek", "../../../data/index", 100)
    # re-ranked search results
    re_ranked_docs = re_rank_docs(hits)

    # Apply evaluation metric for original and re-ranked results

    print(re_ranked_docs[0].docid)


if __name__ == '__main__':
    main()
