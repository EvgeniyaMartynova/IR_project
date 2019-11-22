#Data

This are all the data files collected from the english wikipedia. I used the page https://en.wikipedia.org/wiki/Category:All_disambiguation_pages as main page. For each letter of the alphabet I took the first 200 disambiguation pages (first page for each letter).

## Files
This folder containes a file for each collected page.
The files have the following structure:

```
Title: <Title of Wikipage>
Aspects: {<Title of disambiguation page>}

<Content>
```

## Topic Dictionaries
files can be loaded using 
```
with open("Topics_Pages_A.pkl", 'rb') as f:
    pages = pickle.load(f)
```

and contain a dictionary with the titles of the disambiguation pages as keys and a list of all pages they lead to as values. I think this is usefull for later verification purposes.
