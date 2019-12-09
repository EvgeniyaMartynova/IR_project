
from pyserini.search import pysearch
from . import affinity_ranking as ar

# tunable coefficients for scores linear combination
# alpha query similarity measure score
# beta affinity ranking score
alpha = 0.75
beta = 1 - alpha


class ReRankedDocument:

    def __init__(self, docid, content, score):
        self.docid = docid
        self.content = content
        self.score = score

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
    docs_to_re_rank = list(map(lambda x: ar.Document(x.docid, x.content, x.score), hits))
    af_ranking = ar.get_affinity_ranking(docs_to_re_rank)
    max_similarity_score = hits[0].score
    max_affinity_score = af_ranking[0].score

    re_ranked_documents = []
    for document in af_ranking:
        normalized_similarity_score = document.query_similarity / max_similarity_score
        # for some reason in paper they use log normalization, I do not see a reason for it yet and also with AR
        # we get negative document score because of diversity penalty
        normalized_affinity_score = document.score / max_affinity_score
        final_score = alpha*normalized_similarity_score + beta*normalized_affinity_score
        re_ranked_document = ReRankedDocument(document.docid, document.content, final_score)
        re_ranked_documents.append(re_ranked_document)

    re_ranked_documents.sort(key=lambda x: x.score, reverse=True)
    return re_ranked_documents


def main():
    # Depends on local environment
    # original search results
    hits = extract_docs_for_reranking("Mad dog", "../../../data/index", 30)
    # re-ranked search results
    re_ranked_docs = re_rank_docs(hits)

    # Apply evaluation metric for original and re-ranked results

    print(re_ranked_docs[0].docid)


if __name__ == '__main__':
    main()
