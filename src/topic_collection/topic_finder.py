import os
import pandas as pd

def sort_topics(root_dir):
    filecount = []
    for subdir, dirs, files in os.walk(root_dir):
        if subdir != root_dir:
            nr_files = len(files)
            filecount.append((nr_files, subdir))

    filecount.sort(key=lambda tup: tup[0], reverse=True)
    data = pd.DataFrame(filecount, columns=["Count", "Topic"])
    data["Topic"] = data["Topic"].str.slice(len(root_dir))
    data.to_csv("../../data/TopicCounts.csv", index=False)

def get_top_topics(top):
    data = pd.read_csv("../../data/TopicCounts.csv", nrows=top)
    return data

def main():
    sort_topics('../../../data/Wikipedia Texts/')
    get_top_topics(20)

if __name__ == '__main__':
    main()
