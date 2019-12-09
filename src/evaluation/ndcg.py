import math

path_to_data = "/home/manuela/Uni/jaar_1_Master/Information_Retrieval/IR_project/example data/Topics Aspects/"

def get_relevance(query):
    # open the Topic Aspects file and parse the content
    with open(path_to_data+query+".txt", 'r') as f:
        relevant_docs = f.readlines()
    return [x.split("\t")[0] for x in relevant_docs]


def evaluate(query, hits):
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

def compare_results(query, hits_original, hits_reranked):
    ndcg_original = evaluate(query,hits_original)
    ndcg_reranked = evaluate(query,hits_reranked)
    print("original: " + str(ndcg_original))
    print("reranked: " + str(ndcg_reranked))
