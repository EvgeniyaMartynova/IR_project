
import os

doc_begin = "<DOC>"
doc_end = "</DOC>"

docno_begin = "<DOCNO>"
docno_end = "</DOCNO>"

title_begin = "<TITLE>"
title_end = "</TITLE>"

text_begin = "<TEXT>"
text_end = "</TEXT>"

new_line = "\n"

trec_file_extension = ".trectext"


def build__trec_file_path(output_path, directory):
    return output_path + "/" + os.path.basename(directory) + trec_file_extension


def build__docno(file_name):
    return os.path.splitext(file_name)[0]


def create_trec_directory(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)


def read_file(directory, file_name):
    file_path = directory + "/" + file_name
    file = open(file_path, mode='r')
    file_text = file.read().strip()
    file.close()
    return file_text


def convert_text_to_trec_doc(text, document_number):
    trec_doc = doc_begin + new_line
    trec_doc += docno_begin + document_number + docno_end + new_line
    lines = text.partition('\n\n')
    title = lines[0]
    trec_doc += title_begin + title + title_end + new_line
    body = "".join(lines[2:])
    trec_doc += text_begin + new_line + body + new_line + text_end + new_line
    trec_doc += doc_end + new_line + new_line

    return trec_doc


def convert(documents_path, trec_path):
    folders_num = len(os.listdir(documents_path))
    converted_folders = 0
    for directory, directories, files in os.walk(documents_path):
        has_files = len(files) > 0
        if has_files:
            trec_file = open(build__trec_file_path(trec_path, directory), "w+")
            print("Converting {}".format(directory))
        for file_name in [x for x in files if x.endswith('.txt')]:
            file_text = read_file(directory, file_name)
            docno = build__docno(file_name)
            trec_file.write(convert_text_to_trec_doc(file_text, docno))

        if has_files:
            converted_folders += 1
            print("Converted {} {} % has finished".format(directory, converted_folders * 100/folders_num))
            trec_file.close()

    print("Conversion has been finished!")


def main():
    # TODO:  please change to you local path if run the code from here
    documents_data_path = "../../../data/Wikipedia Texts"
    output_path = "../../../data/trec"
    create_trec_directory(output_path)
    convert(documents_data_path, output_path)

if __name__ == '__main__':
    main()
