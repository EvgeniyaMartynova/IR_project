#Data
This are all the data files collected from the english wikipedia.

## Files
This folder containes a file for each collected page.
The files have the following structure:

Title: <Title of Wikipage>
Aspects: {<Title of disambiguation page>}

followed by the contend of the page.

## Topic Dictionaries
files can be loaded using pickle.load and contain a dictionary with the titles of the disambiguation pages as keys and a list of all pages they lead to as values. I think this is usefull for later verification purposes.
