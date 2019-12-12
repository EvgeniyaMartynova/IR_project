# IR_project

The data set we are going to use is the disambiguated Wikipedia pages. The full data set can be downloaded from Google Drive (I will change it for future). Now we don't have a full collection yet, but I put example_data.zip archive in the root directory of our project - it will work for development purposes.

#### Steps to extract the documents for re-ranking algoruthm 
At the moment the simplest way to extract the documents for re-ranking is implemented, see step 1 from the issue https://github.com/EvgeniyaMartynova/IR_project/issues/8

1. Download the Wikipedia data (or use example_data.zip)
2. To build index only the data from "Wikipedia Texts" folder is needed
3. Conver Wikipedia data to TREC format by running `trec_converter.convert(doc_folder, trec_folder)`. doc_folder is a path to "Wikipedia Texts" folder and trec_folder is a path where you want to put TREC files
4. Build Anserini as described here https://github.com/castorini/anserini
5. The command to build index, run it from the root Anserini folder:
```
nohup sh target/appassembler/bin/IndexCollection -collection TrecCollection -input trec_collection_path -index index_path -generator JsoupGenerator -threads 4 -storePositions -storeDocvectors -storeRawDocs >& log.odp.pos+docvectors+rawdocs &
```
6. Install Pyserini to work with Anserini through Python as described here https://github.com/castorini/pyserini. Note: you migh need to install `Cython` and `wget` first
7. The logic to extract documenst for re-ranking is in 're-ranking.py' file. Extract ranked dosumenst with extract_docs_for_reranking() function and use re_rank_docs() to get re-ranked list
