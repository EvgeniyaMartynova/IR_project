I had to implement precision and recall slightly different to the paper.

Precision now is the number of found relevant documents divided by 10, because we are looking at the top 10 results.
Recall is the number of found relevant topics divided by the total number of relevant topics.

Use evaluate_all(query_list) to evaluate a list of queries at once. The results will be returned in a dataframe with Headers: "Query", "ndcg original", "precision original", "recall original", "F-score original", "ndcg reranked", "precision reranked", "recall reranked", "F-score reranked"

Use evaluate(query) to evaluate a single query. The results are then returned in a single list in the same order as the headers.
