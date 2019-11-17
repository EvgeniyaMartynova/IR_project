
import os

doc_begin = "<DOC>"
doc_end = "</DOC>"

docno_begin = "<DOCNO>"
docno_end = "</DOCNO>"

text_begin = "<TEXT>"
text_end = "</TEXT>"

new_line = "\n"

# TODO: Add tests, clean up

def main():
    opd_data_path = "../../data/opd/texts"
    output_data_path = "../../data/trec"

    for directory, directories, files in os.walk(opd_data_path):
        if len(files) > 0:
            trec_file_path = output_data_path + "/" + os.path.basename(directory) + ".txt"
            trec_file = open(trec_file_path, "w+")
        for file_name in [x for x in files if x.endswith('.txt')]:
            current_document = doc_begin + new_line
            current_document_number = os.path.basename(directory) + "_" + os.path.splitext(file_name)[0]
            current_document += docno_begin + current_document_number + docno_end + new_line
            current_document += text_begin + new_line

            file_path = directory + "/" + file_name
            file = open(file_path, mode='r')
            file_text = file.read()
            file.close()

            current_document += file_text
            current_document += text_end + new_line + doc_end + new_line + new_line

            trec_file.write(current_document)

        if len(files) > 0:
            trec_file.close()





if __name__ == '__main__':
    main()