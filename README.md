# IR_project

The data set we are going to use is the wikified snapshot of ODP. Available at Mendeley Data https://data.mendeley.com/datasets/9mpgz8z257/1

#### Steps to build index of ODP collection with Anserini
1. Download the ODP data from the link above an unzip
2. To build index only the data from "texts" folder is needed
3. Conver ODP data to TREC format by running `trec_converter.convert(odp_folder, trec_folder)`. odp_folder is a path to "texts" ODP folder and trec_folder is a path where you want to put TREC files
4. Build Anserini as described here https://github.com/castorini/anserini
5. Install Pyserini to work with Anserini through Python as described here https://github.com/castorini/pyserini. Note: you migh need to install `Cython` and `wget` first
6. The command to build index, run it from the root Anserini folder:
```
nohup sh target/appassembler/bin/IndexCollection -collection TrecCollection -input trec_collection_path -index index_path -generator JsoupGenerator -threads 4 -storePositions -storeDocvectors -storeRawDocs >& log.odp.pos+docvectors+rawdocs &
```
7. When index is built pass the index folder to pysearch.SimpleSearcher("idex_folder")
