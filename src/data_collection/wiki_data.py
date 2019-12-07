import wikipedia
from bs4 import BeautifulSoup as bs
import requests
import string
import pickle
import os
import uuid
import random
import re
import shutil

data_path = "../../../data"
topics_texts_folder = "Wikipedia Texts"
topics_aspects_folder = "Topics Aspects"

wiki_url = "https://en.wikipedia.org"

abc_list = string.ascii_uppercase
dis_page = wikipedia.WikipediaPage("Category:All disambiguation pages")


def topics_texts_path():
    return data_path + "/" + topics_texts_folder


def topics_aspects_path():
    return data_path + "/" + topics_aspects_folder


def create_topics_texts_directory():
    try:
        path = topics_texts_path()
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)


def create_topics_aspects_directory():
    try:
        path = topics_aspects_path()
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)


def create_topic_directory(topic_title):
    try:
        topic_path = topics_texts_path() + "/" + topic_title
        os.mkdir(topic_path)
        return topic_path
    except OSError:
        print("Creation of the directory %s failed" % topic_path)
        return None


def extract_disambiguation_pages(url):
    page = requests.get(url)
    html = bs(page.text, 'lxml')
    subcategories_html = html.find_all('div', class_='mw-category-group')
    dis_pages = []

    # get disambiguation pages
    for subcategory_html in subcategories_html:
        links = subcategory_html.find_all('a')
        for link in links:
            dis_pages.append((link.get("href"), link.get("title")))
    print(dis_pages)
    return dis_pages


def extract_topics_aspects(disambiguation_page_title):
    try:
        page = wikipedia.page(disambiguation_page_title, auto_suggest=False)
        return None
    except wikipedia.exceptions.DisambiguationError as disambiguation:
        aspects = [title for title in disambiguation.options if "(disambiguation)" not in title]
        return aspects
    except:
        print("Failed to resolve ambiguity %s" % disambiguation_page_title)
        return None


def build_page_path(topic_directory, index):
    return topic_directory + "/" + str(index) + ".txt"


def topic_aspect_path(topic):
    return topics_aspects_path() + "/" + topic + ".txt"


def save_page(page_title, page_content, page_index, topic_directory):
    f = open(build_page_path(topic_directory, page_index), "w+")
    f.write(page_title)
    f.write("\n\n")
    f.write(page_content)
    f.close()


def save_page_topic_aspects(topic, aspects):
    f = open(topic_aspect_path(topic), "w+")
    for aspect, index in aspects:
        f.write(str(index) + "\t" + aspect + "\n")
    f.close()

def download_wiki_data(links):
    create_topics_texts_directory()
    create_topics_aspects_directory()
    for page in links:
        #url = dis_page.url + "?from=" + letter
        url = wiki_url + page
        disambiguation_pages = extract_disambiguation_pages(url)

        # collect links of disambiguation pages
        pages = dict()
        for link, title in disambiguation_pages:
            # remove (disambiguation) from pages that have it and the remaining whitespace
            topic = re.sub('\(disambiguation\)$', '' ,title)
            print(topic)
            aspects = extract_topics_aspects(title)
            if aspects is not None:
                pages[topic] = aspects
        print(pages)

        topics = pages.keys()
        for topic in topics:
            topic_directory = create_topic_directory(topic)
            if topic_directory is not None:
                aspect_pages = pages[topic]
                aspects = []
                for aspect_page in aspect_pages:
                    if aspect_page:
                        try:
                            page = wikipedia.page(aspect_page, auto_suggest=False)
                            page_id = uuid.uuid4()
                            save_page(aspect_page, page.content, page_id, topic_directory)
                            aspects.append((aspect_page, page_id))
                        except wikipedia.exceptions.DisambiguationError:
                            print("Page Error %s" % aspect_page)
                            continue
                        except wikipedia.exceptions.PageError:
                            print("Page non existent %s" % aspect_page)
                            continue
                        except:
                            print("Unknown Error %s" % aspect_page)
                            continue
                if len(aspects) == 0 or len(aspects) == 1:
                    shutil.rmtree(topic_directory)
                else:
                    save_page_topic_aspects(topic, aspects)



def main():
    with open("../Links.pkl", 'rb') as f:
        links = pickle.load(f)
    sample = random.sample(links, 5)
    print(sample)
    download_wiki_data(sample)


if __name__ == '__main__':
    main()
