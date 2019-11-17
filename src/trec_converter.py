
import os

doc_begin = "<DOC>"
doc_end = "</DOC>"

docno_begin = "<DOCNO>"
docno_end = "</DOCNO>"

text_begin = "<TEXT>"
text_end = "</TEXT>"

new_line = "\n"

trec_file_extension = ".trectext"


def build__trec_file_path(output_path, directory):
    return output_path + "/" + os.path.basename(directory) + trec_file_extension


def build__docno(directory, file_name):
    return os.path.basename(directory) + "_" + os.path.splitext(file_name)[0]


def read_file(directory, file_name):
    file_path = directory + "/" + file_name
    file = open(file_path, mode='r')
    file_text = file.read().strip()
    file.close()
    return file_text


def convert_text_to_trec_doc(text, document_number):
    trec_doc = doc_begin + new_line
    trec_doc += docno_begin + document_number + docno_end + new_line
    trec_doc += text_begin + new_line + text + new_line + text_end + new_line
    trec_doc += doc_end + new_line + new_line

    return trec_doc


def convert(opd_path, trec_path):
    for directory, directories, files in os.walk(opd_path):
        has_files = len(files) > 0
        if has_files:
            trec_file = open(build__trec_file_path(trec_path, directory), "w+")
        for file_name in [x for x in files if x.endswith('.txt')]:
            file_text = read_file(directory, file_name)
            docno = build__docno(directory, file_name)
            trec_file.write(convert_text_to_trec_doc(file_text, docno))

        if has_files:
            trec_file.close()

# TODO: pass the paths to a script
def main():
    opd_data_path = "../../data/opd/texts"
    output_path = "../../data/trec"
    convert(opd_data_path, output_path)

if __name__ == '__main__':
    main()