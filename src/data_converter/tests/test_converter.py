from unittest import TestCase
from .. import trec_converter as tc
import os


class TestConverter(TestCase):
    def setUp(self):
        print(os.getcwd())
        for the_file in os.listdir("data_converter/tests/trec"):
            file_path = os.path.join("data_converter/tests/trec", the_file)
            try:
                os.unlink(file_path)
            except Exception as e:
                print(e)

    def test_build__trec_file_path(self):
        output_path = "output/data/trec"
        directory = "input/data/texts/1"
        trec_path = tc.build__trec_file_path(output_path, directory)
        self.assertEqual(trec_path, "output/data/trec/1.trectext")

    def test_build__docno(self):
        file_name = "5.txt"
        docno = tc.build__docno(file_name)
        self.assertEqual(docno, "5")

    def test_convert_text_to_trec_doc(self):
        text = "Title\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " \
               "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. " \
               "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " \
               "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        document_number = "6_99"

        trec_doc = tc.convert_text_to_trec_doc(text, document_number)
        trec_doc_expected = "<DOC>\n" \
                   "<DOCNO>6_99</DOCNO>\n" \
                   "<TITLE>Title</TITLE>\n"\
                   "<TEXT>\n" \
                   "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " \
                   "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. " \
                   "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " \
                   "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n" \
                   "</TEXT>\n" \
                   "</DOC>\n\n"

        self.assertEqual(trec_doc, trec_doc_expected)

    def test_conversion(self):
        tc.convert("data_converter/tests/docs", "data_converter/tests/trec")

        trec_files = os.listdir("data_converter/tests/trec")
        self.assertEqual(len(trec_files), 3)

        for file in trec_files:
            self.assertIn(file, ["1.trectext", "3.trectext", "5.trectext"])

        # compare files content
        for file_name in ["1.trectext", "3.trectext", "5.trectext"]:
            generated_file = open("data_converter/tests/trec/" + file_name, mode='r')
            expected_file = open("data_converter/tests/trec_expected/" + file_name, mode='r')
            self.assertEqual(generated_file.read().strip(), expected_file.read().strip())
            generated_file.close()
            expected_file.close()
