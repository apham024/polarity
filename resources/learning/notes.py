import sys
import os
import numpy
import nltk
from nltk.book import *

# ~/Applications/anaconda/bin/python

NLTK functions
import nltk
nltk.download()

# accessing directories, python directories.py ../corpora/
anaconda/bin/python learning.py parsed_corpora/ output_file.txt
~/Applications/anaconda/bin/python learning.py parsed_corpora/ output_file.txt

#########################################################################################################

text.similar("big") # finds other words that are close to the word "big"
text.concordance("monstrous") # finds all occurences of monstrous in the text 
text.common_contexts(["monstrous", "very"]) # be_glad am_glad a_pretty is_pretty
text.generate() # generates a random text, punctuation is always split off from the last word 
sorted(set(text3)) # grabs tokens of words but dupes are put together
# punctuation goes first, then uppercase, then lowercase
len(set(text)) 
text.count("big") # counts how much the word occurs in a text 
# tokens = number of words in a text, no matter how many times it's repeated
# types = disregards repetitions of a word 
outcome = FreqDist(text) # finds most freq words in the text
vocabulary = outcome.keys() # gives a list of all the distinct types in the text
couplet = ("Rough winds do shake the darling buds of May," # joins 2 strings together without a space 
... 	"And Summer's lease hath all too short a date:")
# to join the strings with a new line, surround it was 3 quotes
# we can use multiplication and addition (without print) but not subtraction or division on strings
# print char, to not print a new line at the end 

Stemmers
# porter correctly maps lying to lie
porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()
[porter.stem(t) for t in tokens]
['DENNI', ':', 'Listen', ',', 'strang', 'women', 'lie', 'in', 'pond', 'distribut', 
'sword', 'is', 'no', 'basi', 'for', 'a', 'system', 'of', 'govern', '.', 'Suprem', 
'execut', 'power', 'deriv', 'from', 'a', 'mandat', 'from',
'the', 'mass', ',', 'not', 'from', 'some', 'farcic', 'aquat', 'ceremoni', '.']
[lancaster.stem(t) for t in tokens]
['den', ':', 'list', ',', 'strange', 'wom', 'lying', 'in', 'pond', 'distribut', 'sword', 
'is', 'no', 'bas', 'for', 'a', 'system', 'of', 'govern', '.', 'suprem', 'execut', 'pow', 'der', 
'from', 'a', 'mand', 'from', 'the', 'mass', ',', 'not', 'from', 'som', 'farc', 'aqu', 'ceremony', '.']

Lemmatization 
#lemmatizer only removes affixes only if the word is in the dictionary 
re.findall(r'\w+|\S\w*', raw) # punctuation is grouped with any following letters (e.g. I'M becomes 'I' and "'M")
# when strings are not segmented and conjoined, we need the bit string that separates the text string to be correctly segmented in to words 

' '.join(text) # joins the list together with a space output inside 
freq_dist = nltk.FreqDist(text) #outputs the frequency of each word 
for word in freq_dist:
	print word, '->', freq_dist[word], ';',


Tokenizing 
from nltk import WordPunctTokenizer
from nltk import TreebankWordTokenizer
from nltk.tag import pos_tag

wpt = WordPunctTokenizer()
tbt = TreebankWordTokenizer()

wpt.tokenize("This is Bob's sandwich.")
['This', 'is', 'Bob', "'", 's', 'sandwich', '.']

tbt.tokenize("This is Bob's sandwich.")
['This', 'is', 'Bob', "'s", 'sandwich', '.']

pos_tag(wpt.tokenize("This is Bob's sandwich."))
[('This', 'DT'), ('is', 'VBZ'), ('Bob', 'NNP'), ("'", 'POS'), ('s', 'NNS'), ('sandwich', 'VBP'), ('.', '.')]

pos_tag(tbt.tokenize("This is Bob's sandwich."))
[('This', 'DT'), ('is', 'VBZ'), ('Bob', 'NNP'), ("'s", 'POS'), ('sandwich', 'NN'), ('.', '.')]

