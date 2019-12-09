import math

path_to_data = "/home/manuela/Uni/jaar_1_Master/Information_Retrieval/IR_project/example data/Topics Aspects/"

def get_relevance(query):
    # open the Topic Aspects file and parse the content
    with open(path_to_data+query+".txt", 'r') as f:
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
    f_score = 2*precision*recall/(precision+recall)

    print("Precision: " + str(precision))
    print("Recall: " + str(recall))
    print("F-Score: " + str(f_score))


def compare_results(query, hits_original, hits_reranked):
    ndcg_original = ndcg(query,hits_original)
    ndcg_reranked = ndcg(query,hits_reranked)
    print("Original Ranking:")
    print("ndcg: " + str(ndcg_original))
    precision_recall_f(query, hits_original)
    print("\nReranked:")
    print("ndcg: " + str(ndcg_reranked))
    precision_recall_f(query, hits_reranked)
