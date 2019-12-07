from unittest import TestCase
from .. import wiki_data as wd
import wikipedia
import os


mea_culpa_aspects = ['Henry Harland', 'Anne Holt', 'David Widgery', 'Mea Maxima Culpa: Silence in the House of God',
                    'Mea Culpa (film)', '"Mea Culpa" (CSI)', 'episode from season 1', 'Ultraviolet (TV serial)',
                     'National Television of Chile', 'Californication', 'Suits (TV series)', 'Sino ang May Sala?: Mea Culpa',
                     'Umbra et Imago', 'Mea Culpa (album)', 'Clementino', 'Mea Culpa (Part II)', 'My Life in the Bush of Ghosts',
                     'Beggar on a Beach of Gold', 'Prison of Desire', 'Nocturne', 'Souf']

clockwork_orange_aspects = ['A Clockwork Orange (novel)', 'A Clockwork Orange (film)', 'A Clockwork Orange (soundtrack)',
                            "A Clockwork Orange: Wendy Carlos's Complete Original Score", 'A Clockwork Orange: A Play with Music',
                            'Clockwork Orange (plot)', 'Glasgow Subway', 'Dutch national football team', 'A Clockwork Origin']

class DataCollectionTests(TestCase):
    def setUp(self):
        print(os.getcwd())
        if os.path.exists("data_collection/tests/docs/A Clockwork Orange.txt"):
            os.remove("data_collection/tests/docs/A Clockwork Orange.txt")

    def test_extract_topic_aspects_is_disambiguation_page(self):
        aspects = wd.extract_topic_aspects("Mea Culpa (disambiguation)")
        self.assertEqual(set(aspects), set(mea_culpa_aspects))


    def test_extract_topic_aspects_non_existing_page(self):
        aspects = wd.extract_topic_aspects("Mea Culpa (disambiguation) error")
        self.assertEqual(aspects, None)


    def test_extract_topic_aspects_not_disambiguation_page(self):
        aspects = wd.extract_topic_aspects("Henry Harland")
        self.assertEqual(aspects, None)

    def test_extract_aspect_page_success(self):
        aspects = wd.extract_aspect_page("Henry Harland")
        self.assertIsInstance(aspects, wikipedia.WikipediaPage)


    def test_extract_aspect_page_disambiguation_exception(self):
        aspects = wd.extract_aspect_page("Mea Culpa (disambiguation)")
        self.assertEqual(aspects, None)


    def test_extract_aspect_page_exception(self):
        aspects = wd.extract_aspect_page("Henry Harland error")
        self.assertEqual(aspects, None)


    def test_extract_topics_with_aspects_all_exist(self):
        topics_with_aspects = wd.extract_topics_with_aspects([("wiki/Mea_Culpa_(disambiguation)", "Mea Culpa (disambiguation)"),
                                                              ("wiki/A_Clockwork_Orange", "A Clockwork Orange")])
        self.assertEqual(len(topics_with_aspects), 2)
        aspects1 = topics_with_aspects["Mea Culpa"]
        self.assertEqual(set(aspects1), set(mea_culpa_aspects))
        aspects2 = topics_with_aspects["A Clockwork Orange"]
        self.assertEqual(set(aspects2), set(clockwork_orange_aspects))


    def test_extract_topics_with_aspects_not_all_exist(self):
        topics_with_aspects = wd.extract_topics_with_aspects([("wiki/Mea_Culpa_(disambiguation)", "Mea Culpa (disambiguation)"),
                                                              ("wiki/A_Clockwork_Orange", "A Clockwork Orange error")])
        self.assertEqual(len(topics_with_aspects), 1)
        aspects1 = topics_with_aspects["Mea Culpa"]
        self.assertEqual(set(aspects1), set(mea_culpa_aspects))


    def test__page_topic_aspects(self):
        extracted_aspects = []
        for i, title in enumerate(clockwork_orange_aspects):
            extracted_aspects.append((title, i))

        wd.save_page_topic_aspects("data_collection/tests/docs/A Clockwork Orange.txt", extracted_aspects)
        generated_file = open("data_collection/tests/docs/A Clockwork Orange.txt", mode='r')
        generated_file_content = generated_file.read().strip()
        generated_file.close()

        expected_file = "0\tA Clockwork Orange (novel)\n" \
                        "1\tA Clockwork Orange (film)\n" \
                        "2\tA Clockwork Orange (soundtrack)\n" \
                        "3\tA Clockwork Orange: Wendy Carlos's Complete Original Score\n" \
                        "4\tA Clockwork Orange: A Play with Music\n" \
                        "5\tClockwork Orange (plot)\n" \
                        "6\tGlasgow Subway\n" \
                        "7\tDutch national football team\n" \
                        "8\tA Clockwork Origin"

        self.assertEqual(generated_file_content, expected_file)



