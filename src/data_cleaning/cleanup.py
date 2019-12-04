import os
rootdir = '/home/manuela/Uni/jaar_1_Master/Information Retrieval/IR_project/newdata/Wikipedia Texts'
apsects = '/home/manuela/Uni/jaar_1_Master/Information Retrieval/IR_project/newdata/Topics Aspects'

def remove_wikitexts():
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path = os.path.join(subdir, file)
            f = open(path, 'r')
            title = f.readline()
            if "page does not exist" in title:
                print(path)
                print(title)
                os.remove(path)
            f.close()

def remove_aspect_entry():
    for file in sorted(os.listdir(apsects)):
        with open(apsects+"/"+file, "r") as f:
            lines = f.readlines()
        with open(apsects+"/"+file, "w") as f:
            for line in lines:
                if "page does not exist" in line:
                    print(file)
                    print(line)
                else:
                    f.write(line)

def remove_small_subfolders():
    for subdir, dirs, files in os.walk(rootdir):
        if subdir != rootdir:
            nr_files = len([name for name in os.listdir(subdir) if os.path.isfile(os.path.join(subdir, name))])
            if nr_files < 2: # can change threshold
                aspect = subdir.replace(rootdir,"")
                print(subdir)
                print(nr_files)
                for file in files:
                    os.remove(os.path.join(subdir,file))
                os.rmdir(subdir)
                os.remove(apsects+aspect+".txt")

remove_wikitexts()
remove_aspect_entry()
remove_small_subfolders()