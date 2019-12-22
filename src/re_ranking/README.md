# Re-ranking implementation

The Affinity Ranking is implemented in affinity_ranking.py and covered by tests that can be found in "tests" folder.

The final re-ranking is implemented in re_ranking.py. To use it extract the documents with `extract_docs_for_reranking` function and pass the results to `re_rank_docs`. See the comments for the detailed usage and `main()` function for the example.
The extraction of the documents is done with Pyserini, so you should have it installed. 