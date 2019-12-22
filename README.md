# IR_project

This project is devoted to implementation and evaluation of the re-ranking of search results for diversity with Affinity Ranking Framework proposed in "[Improving web search results using affinity graph](https://dl.acm.org/citation.cfm?doid=1076034.1076120)" paper.

The document collection we use is extracted from disambiguated Wikipedia pages. The full data set can be downloaded [here](https://drive.google.com/file/d/1U3dbvMyn5j8xODpL3oSw_-A15pzDPhia/view?usp=sharing) and the pre-built index of this collection is available [here](https://drive.google.com/file/d/1pBcWe6V8tIhLA9qADFkOXfrtXCa4u1CJ/view?usp=sharing). The detailed explanation of the relevance judgment and topics/subtopics annotation is given in data_collection's folder readme.

#### Steps to play with re-ranking implementation and evaluation
At the moment the simplest way to extract the documents for re-ranking is implemented, see step 1 from the issue https://github.com/EvgeniyaMartynova/IR_project/issues/8

1. Download the Wikipedia data set from the links given above and pre-build index or build index with the steps given below
2. The re-ranking implementation can be found in /src/re-ranking folder and the code fro evaluation is in /src/evaluation folder. Each folder contains a readme file with the instructions for running the code.
3. The possible queries (titles of disambiguation pages) ordered by the number of relevant documents (pages linked by a disambiguation page) can be found in /queries/TopicCounts.csv and the set of the queries we used for evaluation is in /queries/Final20Queries.csv

#### Steps to build index with Anserini
1. To build index only the data from "Wikipedia Texts" folder is needed
2. Conver Wikipedia data to TREC format by running `trec_converter.convert(doc_folder, trec_folder)` located in /src/data_converter. doc_folder is a path to "Wikipedia Texts" folder and trec_folder is a path where you want to put TREC files
3. Build Anserini as described here https://github.com/castorini/anserini
5. The command to build index, run it from the root Anserini folder:
```
nohup sh target/appassembler/bin/IndexCollection -collection TrecCollection -input trec_collection_path -index index_path -generator JsoupGenerator -threads 4 -storePositions -storeDocvectors -storeRawDocs >& log.odp.pos+docvectors+rawdocs &
```
