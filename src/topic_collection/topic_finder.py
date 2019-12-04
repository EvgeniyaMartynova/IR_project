import os
import pandas as pd

rootdir = '/home/manuela/Uni/jaar_1_Master/Information Retrieval/IR_project/newdata/Wikipedia Texts'

filecount = []
for subdir, dirs, files in os.walk(rootdir):
    if subdir != rootdir:
        nr_files = len(files)
        filecount.append((nr_files,subdir))

filecount.sort(key=lambda tup: tup[0], reverse=True)
data = pd.DataFrame(filecount, columns=["file_nr", "topic"])
data["topic"] = data["topic"].str.replace(rootdir+"/","")
data.to_csv("../../newdata/Topiccounts.csv", index=False)