
from pyserini.search import pysearch

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


def re_rank_docs(query, index_path):
    hits = extract_docs_for_reranking(query, index_path, 1000)
    # Apply affinity re-ranking here
    return hits