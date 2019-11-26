import wikipedia
from bs4 import BeautifulSoup as bs
import requests
import string
import pickle

def get_next_link(link):
    url = link
    page = requests.get(url)
    html = bs(page.text, 'lxml')
    links = html.find_all('a', title='Category:All disambiguation pages')
    page_links = set()
    for link in links:
        if link.text == "next page":
            page_links.add(link.get("href"))

    return page_links

wiki_string = 'https://en.wikipedia.org'
abc_list = string.ascii_uppercase
dis_page = wikipedia.WikipediaPage("Category:All disambiguation pages")
page_links = []

url = dis_page.url+"?from="+abc_list[0]
page_links.append(get_next_link(url).pop())

print(page_links)

for i in page_links:
    url = wiki_string + i
    try:
        link = get_next_link(url).pop()
    except:
        continue
    print(link)
    page_links.append(link)

print()
print(page_links)
with open("Links" + ".pkl", 'wb+') as f:
    pickle.dump(page_links, f, 0)
