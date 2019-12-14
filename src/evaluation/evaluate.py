import sys
sys.path.append('/home/manuela/Uni/jaar_1_Master/Information_Retrieval/IR_project/src')
from re_ranking import re_ranking
import math
import pandas as pd

path_to_data = "/home/manuela/Uni/jaar_1_Master/Information_Retrieval/final data/fixed aspects/"

def get_relevance(query):
    # open the Topic Aspects file and parse the content
    with open(path_to_data+query, 'r') as f:
        relevant_docs = f.readlines()
    return [x.split("\t")[0] for x in relevant_docs]


def ndcg(query, hits):
    relevant_docs = get_relevance(query)
    # the first document is without discount
    if hits[0].docid in relevant_docs:
        ndcg = 1
    else:
        ndcg = 0
    # add the gain of the rest of the list
    for i, hit in enumerate(hits, 1):
        if hit.docid in relevant_docs:
            ndcg += 1/(math.log2(i+1))
    return ndcg

def precision_recall_f(query, hits):
    # get top 10 results
    hits = hits[:10]
    # get all relevant docs for query
    relevant_docs = get_relevance(query)
    # get intersection of relevant docs and top 10 results
    relevant_hits = [hit for hit in hits if hit.docid in relevant_docs]

    precision = len(relevant_hits)/len(hits)
    recall = len(relevant_hits)/len(relevant_docs)
    if precision+recall != 0:
        f_score = 2*precision*recall/(precision+recall)
    else:
        f_score = 0
    return precision, recall, f_score

def compare_results(query, hits_original, hits_reranked):
    ndcg_original = ndcg(query,hits_original)
    ndcg_reranked = ndcg(query,hits_reranked)
    precision_original, recall_original, f_score_original = precision_recall_f(query, hits_original)
    precision_reranked, recall_reranked, f_score_reranked = precision_recall_f(query, hits_reranked)
    results = [query, ndcg_original, precision_original, recall_original, f_score_original, ndcg_reranked, precision_reranked, recall_reranked, f_score_reranked]
    return results

"""Evaluate a single query"""
def evaluate(query, index="../index.final"):
    hits = re_ranking.extract_docs_for_reranking(query, index, 30)
    reranked = re_ranking.re_rank_docs(hits)
    results = compare_results(query, hits, reranked)
    return results

"""Evaluate a list of queries and return results as dataframe object"""
def evaluate_all(query_list, index="../index.final"):
    results = []
    for query in query_list:
        results.append(evaluate(query, index))
    data = pd.DataFrame(results, columns=["Query", "ndcg original", "precision original", "recall original", "F-score original", "ndcg reranked", "precision reranked", "recall reranked", "F-score reranked"])
    return data