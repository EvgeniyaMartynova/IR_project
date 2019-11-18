### A few questions about the data we have

1) First of all we do not have relevance judjment for our collection. How do we evaluate results then? A bit crazy idea I have is to generate searhc queries togeter with relevance judgement from wikification, but I think these RJ will be nor very reliable.
To save time I'm adding the TREC qrels format here:

The format of a qrels file is as follows:

**TOPIC**      **ITERATION**      **DOCUMENT#**      **RELEVANCY** 

where **TOPIC** is the topic number,
**ITERATION** is the feedback iteration (almost always zero and not used),
**DOCUMENT#** is the official document number that corresponds to the "docno" field in the documents, and
**RELEVANCY** is a binary code of 0 for not relevant and 1 for relevant.

Sample Qrels File:

1 0 AP880212-0161 0  
1 0 AP880216-0139 1 
1 0 AP880216-0169 0 
1 0 AP880217-0026 0 
1 0 AP880217-0030 0 

The order of documents in a qrels file is not indicative of relevance or degree of relevance. 
Only a binary indication of relevant (1) or non-relevant (0) is given. 
Documents not occurring in the qrels file were not judged by the human assessor and are assumed to be irrelevant in the evaluations used in TREC. 
The human assessors are told to judge a document relevant if any piece of the document is relevant (regardless of how small the piece is in relation to the rest of the document).

2) In my opinion parsing of the folders structure does not give a good list of topics and aspects. 
Here is the format that TREC Interactive Track use:

**Definition of topics & aspects:**
```
Topic  
|	Aspect# 
|	|	Aspect gloss  
|	|       |   
303i	1	has inspired new cosmological theories  
303i	2	study of gravitational lenses  
303i	3	more precise estimate of scale, size, and age of universe  
303i	4	picture of more distant galaxies/objects  
303i	5	generally good, better, better than expected results  
303i	6	contradicted existing cosmological theories  
303i	7	supported existing cosmological theories  
307i	1	China - Three Gorges, Yangtse, Sanxia  
307i	2	Slovakia- Bos-Nagymaros/Gabcikova/Cunovo  
307i	3	Kenya - Ewaso Ngiro  
307i	4	Mexico - Rio Usumacinta  
307i	5	Canada - James Bay/Great Whale  
307i	6	Iran - Karun  
307i	7	India - Narmada  
307i	8	Kyrgyzstan - Naryn  
307i	9	Chile - Panque/Bo-Bo/Bio-Bio 
```

**Mapping of the documents to the topicts and aspects**
```
Topic  
|   Document  
|	  |	        Aspect vector:                1 digit/aspect  
|	  |	        |	                            leftmost digit = aspect #1  
|	  |	        |	                            "1" = "aspect covered by this doc."  
303i FT921-3432		0000000  
303i FT924-286		1111000  
303i FT934-5418		0000100  
303i FT941-15661	0000100  
303i FT944-128		0011111  
303i FT944-9936		0000000  
307i FT911-3434		10000000000000000000000  
307i FT911-3436		10000000000000000000000
```

I think we can get a similar representation exploiting wikification.

3) Also we do not have the sample queries. How do we create them? 


