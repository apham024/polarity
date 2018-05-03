#!/usr/bin/python
import sys, operator, string, os, fileinput
import nltk
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

##############################################################################################################

# http://www.clips.ua.ac.be/pages/pattern-examples-100days

input_filename = sys.argv[1] # reads the "clean" output file
output_filename = sys.argv[2]
# word_dict[words] = {}

def word_dict(sentence_token, line_list, output_filename):  

	word_dict[words] = {}

	# pos_dict = {'good', 'awesome', 'superb', 'amazing', 'dream', 'welcome'}
	# neutral_dict = {'Obama', 'Trump', 'Clinton', 'Sanders', 'president', 'Democrat', 'Republican', 'election', 'voter', 'America'}
	# neg_dict = {'explosion', 'deport', 'insult', 'ridiculous', 'disappointing', 'immigrant'}

	output_filehandle = open(output_filename, 'r')

	for sentence_token in line_list:
		if sentence_token not in word_dict:
			word_dict[word].append(sentence_token)
			word_dict[word] = word_dict[word] + 1

		elif sentence_token in word_dict:
			#skip adding 
			word_dict[word] = word_dict[word] + 1

	
	output_filehandle.close()	
