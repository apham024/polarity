import os, sys

def get_corpus_path_dictionary(top_directory):

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
			corpus_tokens_list_dictionary[network_name] = {} # list of tokens inside each date file in the date folder
			
			for date in date_list: # the document files in the date folder 

				if not date in ignore_dictonary:

					date_path = top_directory + network_name + "/" + date # 'parsedcorpora/CNN/CNN_20121111-20121117'
					corpus_list = os.listdir(date_path) # the individual document files in the date folder
					filename_list_dictionary[network_name][date] = [] # creates a dictionary of network lists (cnn, abcnews, etc.) and date lists (CNN_20121111-20121117)
					corpus_tokens_list_dictionary[network_name][date] = [] #  # list of tokens inside each date file in the date folder

					for corpus in corpus_list: # for each document file in the document file list

						if not corpus in ignore_dictonary:

							corpus_path = top_directory + network_name + "/" + date + "/" + corpus # 'parsedcorpora/CNN/CNN_20121111-20121117/CNN_20121111-20121117_000'
							filename_list_dictionary[network_name][date].append(corpus_path) 
							corpus_tokens_list_dictionary[network_name][date].append([])

	return filename_list_dictionary


def process_corpora(filename_list_dictionary, corpus_tokens_list_dictionary):

	for corpus in filename_list_dictionary:

		for date in corpus:

			for file in date:

				print file # 'abcnews/ABC_20121111-20121117/ABC_20121111-20121117_000'

				current_filehandle = open(file)

				# your function calls go here, processing the current corpus file
				# resulting in a single stemmed line list
				document_line_list = remove_speaker(input_filename)
				cleaned_line_list = clean_lines(document_line_list)
				word_list, word_freq_dict = count_freqs(cleaned_line_list)
				stemmed_line_list = stemmed_line(cleaned_line_list)
				output_final_document(stemmed_line_list, output_filename)


				corpus_tokens_list_dictionary[corpus][date][file] = stemmed_line_list

	input_path = sys.argv[1]
	filename_list_dictionary = get_corpus_path_dictionary(input_path)
	process_corpora(filename_list_dictionary, corpus_tokens_list_dictionary[corpus][date][file])


