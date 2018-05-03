#!/usr/bin/python
import sys, operator, string, os, fileinput
import nltk
from nltk.tag import pos_tag
from nltk import TreebankWordTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

##############################################################################################################

input_path = sys.argv[1]
output_filename = sys.argv[2]

def get_corpus_path_dictionary(top_directory):
# top_directory = sys.argv[1]

# similar to a 4D matrix
# each row is a network name and each column is a date 
# inside each cell, is a date folder with a list of document file corpora

	ignore_dictonary = {}
	ignore_dictonary['.DS_Store'] = 1
	ignore_dictonary['Icon\r'] = 1

	filename_list_dictionary = {}
	corpus_tokens_list_dictionary = {}

	network_list = os.listdir(top_directory) # top directory is parsedcorpora

	for network_name in network_list: # cnn, abcnews, foxnews, msnbc

		if not network_name in ignore_dictonary:  # gets rid of invisible junk 

			network_path = top_directory + network_name # parsedcorpora/abcnews
			date_list = os.listdir(network_path) # list of folders of each date in each network folder
			filename_list_dictionary[network_name] = {} # creates a dictionary of network name lists (abcnews, cnn, etc.)
			corpus_tokens_list_dictionary[network_name] = {} # list of tokens (or files) inside each date file in the date folder

			for date in date_list: # the document files in the date folder 

				if not date in ignore_dictonary:

					date_path = top_directory + network_name + "/" + date # 'parsedcorpora/CNN/CNN_20121111-20121117'
					
					corpus_list = os.listdir(date_path) # the individual document files in the date folder
					filename_list_dictionary[network_name][date] = [] # adds date lists (CNN_20121111-20121117) into dictionary with network names
					corpus_tokens_list_dictionary[network_name][date] = [] 

					for corpus in corpus_list: # for each document file in the document file list

						if not corpus in ignore_dictonary:

							corpus_path = top_directory + network_name + "/" + date + "/" + corpus # 'parsedcorpora/CNN/CNN_20121111-20121117/CNN_20121111-20121117_000'
							filename_list_dictionary[network_name][date].append(corpus_path) 
							corpus_tokens_list_dictionary[network_name][date].append([])


	return filename_list_dictionary, corpus_tokens_list_dictionary

##############################################################################################################

def remove_speaker(input_filename):
	document_line_list = []

	input_filehandle = open(input_filename)
	for line in input_filehandle:
		cleaned_line = line.strip('\n').strip('\r').strip() # strips newline and white space
		split_line = cleaned_line.split(':')  # takes out :
		stripped_line = (''.join(split_line[1:])).strip() # joins the line after the first occurrence and conjoins them with a ' ' in between

		#if len(stripped_line) > 0:

		output_line = filter(None, stripped_line) # takes out empty stings in the list
		document_line_list.append(output_line)

	input_filehandle.close()

	return document_line_list

##############################################################################################################

def clean_lines(line_list):
	# line_list = []
	cleaned_list = []
	for line in line_list:
		tokens = nltk.word_tokenize(line) # splits contractions 

		for i in range(len(tokens)):
			tokens[i] = tokens[i].lower()

		cleaned_list.append(tokens)

	return cleaned_list

##############################################################################################################

def stemmed_line(cleaned_line_list): 
	stemmed_line_list = [] # new changed line after tokenizing 
	tbt = TreebankWordTokenizer()
	#test_line = "That's Bob's dog!"

	for line_list in cleaned_line_list: 
		for token in line_list:
			tokenized_line = tbt.tokenize(token) # line is a list and tokenize does not take a list
			stemmed_line_list.append(tokenized_line)

	# print tokenized_line
	return stemmed_line_list


##############################################################################################################

def output_processed_corpora(file, cleaned_line_list, output_filename):
	
	output_filehandle = open(output_filename, 'a')


	output_filehandle.write(file)

	for sentence in cleaned_line_list:
		output_string = (' '.join(sentence))
		output_filehandle.write(" %s" % output_string) # writes the path name to the file 
	output_filehandle.write('\n')
	output_filehandle.close()	


##############################################################################################################

def process_corpora(filename_list_dictionary, corpus_tokens_list_dictionary):
	corpus_tokens_list_dictionary = {}
	for corpus in filename_list_dictionary: # abcnews
		for date in filename_list_dictionary[corpus]: # ABC_20121111-20121117
			for file in filename_list_dictionary[corpus][date]: # each document in the date folder 
	
				document_line_list = remove_speaker(file) # removes speaker  
				cleaned_line_list = clean_lines(document_line_list)[1:] # splits the contractions

				output_processed_corpora(file, cleaned_line_list, output_filename) 


##############################################################################################################

filename_list_dictionary, corpus_tokens_list_dictionary = get_corpus_path_dictionary(input_path)
process_corpora(filename_list_dictionary, corpus_tokens_list_dictionary)

##############################################################################################################

