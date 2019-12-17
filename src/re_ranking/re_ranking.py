
from pyserini.search import pysearch
import affinity_ranking as ar
import matplotlib.pyplot as plt
import numpy as np

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

    fig = plt.figure()
    fig.tight_layout()
    subplot = fig.add_subplot(111)
    subplot.set_xlabel('Document', fontdict={'fontsize': 11, 'fontweight': 'bold'})
    subplot.set_ylabel('Score', fontdict={'fontsize': 11, 'fontweight': 'bold'})
    subplot.spines['top'].set_color('none')
    subplot.spines['bottom'].set_color('none')
    subplot.spines['left'].set_color('none')
    subplot.spines['right'].set_color('none')
    subplot.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

    subplot1 = fig.add_subplot(311)
    plt.plot(t, original_scores)
    subplot1.title.set_text('Query similarity')
    subplot1.title.set_fontsize(11)

    subplot2 = fig.add_subplot(312)
    plt.plot(t, affinity_scores)
    subplot2.title.set_text('Affinity')
    subplot2.title.set_fontsize(11)

    subplot3 = fig.add_subplot(313)
    plt.plot(t, re_ranked_scores)
    subplot3.title.set_text('Re-ranked')
    subplot3.title.set_fontsize(11)
    plt.subplots_adjust(hspace=0.7)
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


def re_rank_docs(hits, alpha=0.75, plot=False):
    beta = 1 - alpha
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
    if plot:
        plot_scores(hits, ar_documents, re_ranked_documents)

    return re_ranked_documents


def main():
    # Depends on local environment
    # original search results
    hits = extract_docs_for_reranking("St. Mary's Church", "../../../data/index", 300)
    # re-ranked search results
    re_ranked_docs = re_rank_docs(hits, plot=True)



if __name__ == '__main__':
    main()
