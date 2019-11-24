#Data

This are all the data files collected from the english wikipedia. I used the page https://en.wikipedia.org/wiki/Category:All_disambiguation_pages as main page. For each letter of the alphabet I took the first 200 disambiguation pages (first page for each letter).

We translate wikipedia disambiguation pages into "topic -> aspects" model the following way. Each page is a topic and all the disambiguating links for this page are treated as aspects. Due to the format of wikipedia disambiguation pages each file can have only one aspect (becuase the file itself is the aspect). The data format we get is the following:

## Wikipedia Texts
This folder containes topics subfolders with the content of disambiguating pages as files. An UUID is used for naming files, because it is used as a DOCNO when the data are converted to TREC format (it was the most straightforward way to create a unique document number).

```
Wikipedia Texts
---- Topic1
-------- UUID1.txt
-------- UUID2.txt
---- Topic2
-------- UUID3.txt
```

## Topics Aspects
This folder contains the infromation about the aspects of each topic and maps aspects to files. There is a text file which corresponds to each topic and have the following structure: 
```
Docid   aspect
  |     |
UUID1   aspect 1
UUID2   aspect 2
```
