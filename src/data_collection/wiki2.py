import wikipedia
from bs4 import BeautifulSoup as bs
import requests
import string
from collections import defaultdict
import pickle

index = 0
abc_list = string.ascii_uppercase
dis_page = wikipedia.WikipediaPage("Category:All disambiguation pages")

for i in range(0, len(abc_list)):
    url = dis_page.url+"?from="+abc_list[i]
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


    # collect links of disambiguation pages
    pages = dict()
    for link, title in dis_pages:
        print(title)
        wiki_string = "https://en.wikipedia.org"
        url = wiki_string + link
        page = requests.get(url)
        html = bs(page.text, 'lxml')
        page_links = html.find('ul').find_all('li')
        sub_pages = []
        for links in page_links:
            ref_link = links.find('a')
            if ref_link:
                sub_pages.append((ref_link.get("href"), ref_link.get("title")))
        pages[title] = sub_pages
    print(pages)
    with open("Topics_Pages_" + abc_list[i] + ".pkl", 'wb+') as f:
        pickle.dump(pages, f, 0)

    # invert dictionary
    inverted_pages = defaultdict(set)
    for key, link_list in pages.items():
        for i in link_list:
            inverted_pages[i].add(key)
    print()
    print(inverted_pages)

    #store pages
    for page, aspects in inverted_pages.items():
        page_title = page[1]
        if page_title:
            try:
                page = wikipedia.page(page_title)
            except wikipedia.exceptions.DisambiguationError:
                print("Page Error")
                continue
            except wikipedia.exceptions.PageError:
                print("Page non existent")
                continue
            except:
                print("Unknown Error")
            f = open("Data/"+str(index)+".txt", "w+")
            f.write("Title: "+ page.title)
            f.write("\n")
            f.write("Aspects: "+str(aspects))
            f.write("\n\n")
            f.write(page.content)
            f.close()
            index += 1