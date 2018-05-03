
import sys, os, time, datetime, shutil, math, operator
import numpy as np
################################################################################################
################################################################################################
target_filename = sys.argv[1]
control_filename = sys.argv[2]
dimension_filename = sys.argv[3]
corpus_filename = sys.argv[4]
window_size = int(sys.argv[5])
output_diretory = sys.argv[6]
################################################################################################
################################################################################################
class Valence_Matrix:
	############################################################################################
	def __init__(self):

		self.corpus_filename = 0
		self.document_list = []
		self.document_size_matrix = []
		self.num_documents = 0

		self.source_list = []
		self.source_index_dict = {}
		self.num_sources = 0
		self.date_list = []
		self.date_index_dict = {}
		self.num_dates = 0

		self.dimension_list = []
		self.dimension_index_dict = {}
		self.num_dimensions = 0
		self.dimension_weights = []
		self.dimension_freq_matrix = []

		self.target_list = []
		self.target_index_dict = {}
		self.num_targets = 0
		self.target_freq_matrix = []

		self.control_list = []
		self.control_index_dict = {}
		self.num_controls = 0
		self.control_freq_matrix = []

		self.window_size = 0
		self.target_dimension_cooc_matrix = []

	############################################################################################
	def get_dimension_info(self, dimension_filename):

		dimension_filehandle = open(dimension_filename)
		for line in dimension_filehandle:
			data = (line.strip().strip('\n').strip()).split()
			dimension = data[-1]
			if len(data) > 1:
				value = float(data[0])
			else:
				value = 1
			if not dimension in self.dimension_index_dict:
				self.dimension_list.append(dimension)
				self.dimension_index_dict[dimension] = self.num_dimensions
				self.num_dimensions += 1
				self.dimension_weights.append(value)
		dimension_filehandle.close()

	############################################################################################
	def get_target_info(self, target_filename):

		target_file = open(target_filename)
		for line in target_file:
			target = line.strip().strip('\n').strip()
			if not target in self.target_index_dict:
				self.target_list.append(target)
				self.target_index_dict[target] = self.num_targets
				self.num_targets += 1
		target_file.close()

	############################################################################################
	def get_control_info(self, control_filename):

		control_file = open(control_filename)
		for line in control_file:
			control = line.strip().strip('\n').strip()
			if not control in self.control_index_dict:
				self.control_list.append(control)
				self.control_index_dict[control] = self.num_controls
				self.num_controls += 1
		control_file.close()

	############################################################################################
	def build_empty_matrices(self, corpus_filename):
		
		self.corpus_filename = corpus_filename
		corpus_filehandle = open(self.corpus_filename)

		for line in corpus_filehandle:

			self.num_documents += 1

			data = (line.strip('\n').strip()).split()
			token_list = data[1:]
			document_info = (data[0].split("/")[-1]).split("_")
			source = document_info[0]
			unformatted_date = document_info[1].split("-")[0]
			date = unformatted_date[0:4] + "-" + unformatted_date[4:6] + "-" + unformatted_date[6:8]

			document = int(document_info[2])

			if not source in self.source_index_dict:
				self.source_list.append(source)
				self.source_index_dict[source] = self.num_sources
				self.num_sources += 1

			if not date in self.date_index_dict:
				self.date_list.append(date)
				self.date_index_dict[date] = self.num_dates
				self.num_dates += 1

		corpus_filehandle.close()

		self.dimension_freq_matrix = np.zeros([self.num_sources, self.num_dates, self.num_dimensions], int)
		self.target_freq_matrix = np.zeros([self.num_sources, self.num_dates, self.num_targets], int)
		self.control_freq_matrix = np.zeros([self.num_sources, self.num_dates, self.num_controls], int)
		self.target_dimension_cooc_matrix = np.zeros([self.num_sources, self.num_dates, self.num_targets, self.num_dimensions], int)
		self.control_dimension_cooc_matrix = np.zeros([self.num_sources, self.num_dates, self.num_controls, self.num_dimensions], int)
		self.document_size_matrix = np.zeros([self.num_sources, self.num_dates], int)

		print
		print "Creating Empty Valence Matrix with:"
		print "		%s Target Words" % self.num_targets
		print "		%s Control Words" % self.num_controls
		print "		%s Dimension Words" % self.num_dimensions
		print "		%s Corpus Sources" % self.num_sources
		print "		%s Corpus Dates" % self.num_dates
		print "		%s Total Documents" % self.num_documents
		print

	###########################################################################################
	def count_coocs(self, window_size):

		self.window_size = window_size

		print "Counting Target-Dimension Co-occurrences"

		corpus_filehandle = open(self.corpus_filename)

		line_counter = 0
		self.total_tokens = 0

		for line in corpus_filehandle:
			line_counter += 1

			data = (line.strip('\n').strip()).split()
			token_list = data[1:]
			document_info = (data[0].split("/")[-1]).split("_")
			source = document_info[0]
			source_index = self.source_index_dict[source]
			unformatted_date = document_info[1].split("-")[0]
			date = unformatted_date[0:4] + "-" + unformatted_date[4:6] + "-" + unformatted_date[6:8]
			date_index = self.date_index_dict[date]
			document = int(document_info[2])

			start_time = time.time()

			window = []

			for token in token_list:
				
				self.document_size_matrix[source_index, date_index] += 1
				self.total_tokens += 1

				window.append(token)
				
				if len(window) >= self.window_size+1:
				
					if ((window[0] in self.target_index_dict) or (window[0] in self.dimension_index_dict) or (window[0] in self.control_index_dict)):
				
						if window[0] in self.target_index_dict:
							self.target_freq_matrix[source_index, date_index, self.target_index_dict[window[0]]] += 1
							
						if window[0] in self.dimension_index_dict:
							self.dimension_freq_matrix[source_index, date_index, self.dimension_index_dict[window[0]]] += 1

						if window[0] in self.control_index_dict:
							self.control_freq_matrix[source_index, date_index, self.control_index_dict[window[0]]] += 1
								
						for i in range(len(window)-1):

							if ((window[0] in self.target_index_dict) and (window[i+1] in self.dimension_index_dict)):
								self.target_dimension_cooc_matrix[source_index, date_index, self.target_index_dict[window[0]], self.dimension_index_dict[window[i+1]]] += 1       

							elif ((window[0] in self.dimension_index_dict) and (window[i+1] in self.target_index_dict)):
								self.target_dimension_cooc_matrix[source_index, date_index, self.target_index_dict[window[i+1]], self.dimension_index_dict[window[0]]] += 1

							elif ((window[0] in self.control_index_dict) and (window[i+1] in self.dimension_index_dict)):
								self.control_dimension_cooc_matrix[source_index, date_index, self.control_index_dict[window[0]], self.dimension_index_dict[window[i+1]]] += 1       

							elif ((window[0] in self.dimension_index_dict) and (window[i+1] in self.control_index_dict)):
								self.control_dimension_cooc_matrix[source_index, date_index, self.control_index_dict[window[i+1]], self.dimension_index_dict[window[0]]] += 1

					window = window[1:]


			# flush the remainder of the window, same code as above
			while len(window) > 0:

				if ((window[0] in self.target_index_dict) or (window[0] in self.dimension_index_dict) or (window[0] in self.control_index_dict)):
			
					if window[0] in self.target_index_dict:
						self.target_freq_matrix[source_index, date_index, self.target_index_dict[window[0]]] += 1
						
					if window[0] in self.dimension_index_dict:
						self.dimension_freq_matrix[source_index, date_index, self.dimension_index_dict[window[0]]] += 1

					if window[0] in self.control_index_dict:
						self.control_freq_matrix[source_index, date_index, self.control_index_dict[window[0]]] += 1
							
					for i in range(len(window)-1):

						if ((window[0] in self.target_index_dict) and (window[i+1] in self.dimension_index_dict)):
							self.target_dimension_cooc_matrix[source_index, date_index, self.target_index_dict[window[0]], self.dimension_index_dict[window[i+1]]] += 1       

						elif ((window[0] in self.dimension_index_dict) and (window[i+1] in self.target_index_dict)):
							self.target_dimension_cooc_matrix[source_index, date_index, self.target_index_dict[window[i+1]], self.dimension_index_dict[window[0]]] += 1

						elif ((window[0] in self.control_index_dict) and (window[i+1] in self.dimension_index_dict)):
							self.control_dimension_cooc_matrix[source_index, date_index, self.control_index_dict[window[0]], self.dimension_index_dict[window[i+1]]] += 1       

						elif ((window[0] in self.dimension_index_dict) and (window[i+1] in self.control_index_dict)):
							self.control_dimension_cooc_matrix[source_index, date_index, self.control_index_dict[window[i+1]], self.dimension_index_dict[window[0]]] += 1

				window = window[1:]

	 		if line_counter % 10 == 0:
	 			took = time.time() - start_time
	 			print "		Finished %s Documents and %s Tokens 		(%0.2f sec)" % (line_counter, self.total_tokens, took)
	 	print
	
	 ###########################################################################################
	def output_data(self, output_directory):

		###########################################################################################
		def output_valence_matrix_info():

		 	matrix_info_filehandle = open(output_directory+"/valence_matrix_info.txt", "w")
		 	matrix_info_filehandle.write("NUM_TARGETS: %s\n" % self.num_targets)
		 	matrix_info_filehandle.write("NUM_CONTROLS: %s\n" % self.num_controls)
		 	matrix_info_filehandle.write("NUM_DIMENSIONS: %s\n" % self.num_dimensions)
		 	matrix_info_filehandle.write("NUM_DOCUMENTS: %s\n" % self.num_documents)
		 	matrix_info_filehandle.write("NUM_TOKENS: %s\n" % self.total_tokens)
		 	matrix_info_filehandle.write("NUM_SOURCES: %s\n" % self.num_sources)
		 	matrix_info_filehandle.write("NUM_DATES: %s\n" % self.num_dates)
		 	matrix_info_filehandle.close()

		 ###########################################################################################
		def output_document_info():
		 	document_info_filehandle = open(output_directory+"/document_matrix_info.txt", "w")
		 	document_info_filehandle.write("source, date, num_tokens\n")
	 		for i in range(self.num_sources):
	 			for j in range(self.num_dates):

	 				document_info_filehandle.write("%s, %s, %s\n" % (self.source_list[i], self.date_list[j], self.document_size_matrix[i,j]))

	 				if self.document_size_matrix[i,j] == 0:
	 					print "		WARNING, Document %s %s has a size of 0. Many errors will occur..." % (self.source_list[i], self.date_list[j])
	 		document_info_filehandle.close()

	 	###########################################################################################
	 	def output_target_info():
	 		target_info_filehandle = open(output_directory+"/target_info.txt", "w")
	 		target_info_filehandle.write("target, source, date, freq, lfreq, ppm, lppm\n")
	 		for i in range(self.num_targets):
	 			for j in range(self.num_sources):
	 				for k in range(self.num_dates):
	 					freq = self.target_freq_matrix[j,k,i]
	 					if freq > 0:
	 						lfreq = math.log10(freq)
	 					else:
	 						lfreq = 0
	 					document_size = self.document_size_matrix[j,k]
	 					log_document_size = math.log10(document_size)
	 					ppm = 1000000 * (float(freq) / document_size)
	 					lppm = 1000000 * (float(lfreq) / log_document_size)

	 					target_info_filehandle.write("%s, %s, %s, %s, %0.4f, %0.2f, %0.2f\n" % (self.target_list[i], self.source_list[j], self.date_list[k], freq, lfreq, ppm, lppm))

	 		target_info_filehandle.close()

	 	###########################################################################################
	 	def output_control_info():
	 		control_info_filehandle = open(output_directory+"/control_info.txt", "w")
	 		control_info_filehandle.write("control, source, date, freq, lfreq, ppm, lppm\n")
	 		for i in range(self.num_controls):
	 			for j in range(self.num_sources):
	 				for k in range(self.num_dates):
	 					freq = self.control_freq_matrix[j,k,i]
	 					if freq > 0:
	 						lfreq = math.log10(freq)
	 					else:
	 						lfreq = 0
	 					document_size = self.document_size_matrix[j,k]
	 					log_document_size = math.log10(document_size)
	 					ppm = 1000000 * (float(freq) / document_size)
	 					lppm = 1000000 * (float(lfreq) / log_document_size)

	 					control_info_filehandle.write("%s, %s, %s, %s, %0.4f, %0.2f, %0.2f\n" % (self.control_list[i], self.source_list[j], self.date_list[k], freq, lfreq, ppm, lppm))

	 		control_info_filehandle.close()

	 	###########################################################################################
	 	def output_dimension_info():
	 		dimension_info_filehandle = open(output_directory+"/dimension_info.txt", "w")

	 		dimension_info_filehandle.write("dimension, source, date, freq, lfreq, ppm, lppm\n")
	 		for i in range(self.num_dimensions):
	 			for j in range(self.num_sources):
	 				for k in range(self.num_dates):
	 					freq = self.dimension_freq_matrix[j,k,i]
	 					if freq > 0:
	 						lfreq = math.log10(freq)
	 					else:
	 						lfreq = 0
	 					document_size = self.document_size_matrix[j,k]
	 					log_document_size = math.log10(document_size)
	 					ppm = 1000000 * (float(freq) / document_size)
	 					lppm = 1000000 * (float(lfreq) / log_document_size)

	 					dimension_info_filehandle.write("%s, %s, %s, %s, %0.4f, %0.2f, %0.2f\n" % (self.dimension_list[i], self.source_list[j], self.date_list[k], freq, lfreq, ppm, lppm))

	 		dimension_info_filehandle.close()

	 	###########################################################################################
	 	def output_target_dimension_coocs():
	 		target_dimension_coocs_filehandle = open(output_directory+"/target_dimension_coocs.txt", "w")

	 		target_dimension_coocs_filehandle.write("target, dimension, source, date, cooc, lcooc, pim, lpim\n")
	 		for h in range(self.num_targets):
				for i in range(self.num_dimensions):
					for j in range(self.num_sources):
						for k in range(self.num_dates):

							cooc = self.target_dimension_cooc_matrix[j,k,h,i]
							if cooc > 0:
								lcooc = math.log10(cooc)
							else:
								lcooc = 0

							target_freq = self.target_freq_matrix[j,k,h]
							if target_freq > 0:
	 							target_lfreq = math.log10(target_freq)
	 						else:
	 							lfreq = 0

	 						dimension_freq = self.dimension_freq_matrix[j,k,i]
	 						if dimension_freq > 0:
	 							dimension_lfreq = math.log10(dimension_freq)
	 						else:
	 							dimension_lfreq = 0

							document_size = self.document_size_matrix[j,k]
							max_possible_coocs = (self.window_size * document_size * 2) - (self.window_size**2 + self.window_size)

							cooc_prob = float(cooc) / max_possible_coocs
							target_prob = float(target_freq) / document_size
							dimension_prob = float(dimension_freq) / document_size

							if cooc > 0:
								cooc_lprob = math.log10(cooc) / math.log10(max_possible_coocs)
							else:
								cooc_lprob = 0

							if target_freq > 0:
								target_lprob = math.log10(target_freq) / math.log10(document_size)
							else:
								target_lprob = 0

							if dimension_freq > 0:
								dimension_lprob = math.log10(dimension_freq) / math.log10(document_size)
							else:
								dimension_lprob = 0

							try:
								pim = math.log10((cooc_prob) / (target_prob*dimension_prob))
							except:
								pim = 0

							try:
								lpim = math.log10((cooc_lprob) / (target_lprob*dimension_lprob))
							except:
								lpim = 0

							target_dimension_coocs_filehandle.write("%s, %s, %s, %s, %0.4f, %0.4f, %0.4f, %0.4f\n" % (self.target_list[h], self.dimension_list[i], self.source_list[j], self.date_list[k], cooc, lcooc, pim, lpim))

	 		target_dimension_coocs_filehandle.close()

	 	###########################################################################################
	 	def output_valence_scores():

	 		valence_scores_filehandle = open(output_directory+"/valence_scores.txt", "w")
	 		valence_scores_filehandle.write("source, date, target, freq, coocprob_score, pim_score, coocprob_zscore, pim_zscore\n")

	 		for i in range(self.num_sources):

	 			for j in range(self.num_dates):

	 				document_size = self.document_size_matrix[i,j]
	 				max_possible_coocs = (self.window_size * document_size * 2) - (self.window_size**2 + self.window_size)

	 				control_coocprob_scores = np.zeros([self.num_controls], float)
	 				control_pim_scores = np.zeros([self.num_controls], float)

	 				for control_counter in range(self.num_controls):

	 					cooc_score = 0
	 					pim_score = 0

	 					control_freq = self.control_freq_matrix[i,j,control_counter]
	 					control_prob = float(control_freq) / document_size

	 					for dimension_counter in range(self.num_dimensions):

	 						dimension_freq = self.dimension_freq_matrix[i,j,dimension_counter]
	 						dimension_prob = float(dimension_freq) / document_size

	 						control_cooc = self.control_dimension_cooc_matrix[i,j,control_counter,dimension_counter]
							control_cooc_prob = float(control_cooc) / max_possible_coocs

							try:
								control_pim = math.log10((control_cooc_prob) / (control_prob*dimension_prob))
							except:
								control_pim = 0

							control_coocprob_scores[control_counter] += control_cooc_prob * self.dimension_weights[dimension_counter]
							control_pim_scores[control_counter] +=  control_pim * self.dimension_weights[dimension_counter]

					control_coocprob_mean = control_coocprob_scores.mean()
					control_pim_mean = control_pim_scores.mean()
					control_coocprob_std = control_coocprob_scores.std()
					control_pim_std = control_pim_scores.std()

	 				for k in range(self.num_targets):

	 					coocprob_score = 0
	 					pim_score = 0

	 					target_freq = self.target_freq_matrix[i,j,k]
	 					target_prob = float(target_freq) / document_size

	 					for dimension_counter in range(self.num_dimensions):

	 						dimension_freq = self.dimension_freq_matrix[i,j,dimension_counter]
	 						dimension_prob = float(dimension_freq) / document_size

	 						cooc = self.target_dimension_cooc_matrix[i,j,k,dimension_counter]
							cooc_prob = float(cooc) / max_possible_coocs

							try:
								pim = math.log10((cooc_prob) / (target_prob*dimension_prob))
							except:
								pim = 0

							coocprob_score += cooc_prob * self.dimension_weights[dimension_counter]
	 						pim_score +=  pim * self.dimension_weights[dimension_counter]

	 					freq = (target_freq / float(document_size)) * 1000000
	 					coocprob_score = coocprob_score / self.num_dimensions
	 					pim_score = pim_score / self.num_dimensions

	 					coocprob_zscore = (coocprob_score - control_coocprob_mean) / control_coocprob_std
	 					pim_zscore = (pim_score - control_pim_mean) / control_pim_std

	 					valence_scores_filehandle.write("%s, %s, %s, %0.2f, %s, %0.3f, %0.3f, %0.3f\n"% (self.source_list[i], self.date_list[j], self.target_list[k], freq, coocprob_score, pim_score, coocprob_zscore, pim_zscore))
	 		valence_scores_filehandle.close()

	 	###########################################################################################

 		try:
	 		os.mkdir(output_directory)
	 	except:
	 		print "ERROR, could not create directory %s" % output_directory
	 	output_valence_matrix_info()
	 	output_document_info()
	 	output_target_info()
	 	output_control_info()
	 	output_dimension_info()
	 	output_target_dimension_coocs()
	 	output_valence_scores()

##############################################################################################################################
##############################################################################################################################
def main():
	the_valence_matrix = Valence_Matrix()
	the_valence_matrix.get_target_info(target_filename)
	the_valence_matrix.get_control_info(control_filename)
	the_valence_matrix.get_dimension_info(dimension_filename)
	the_valence_matrix.build_empty_matrices(corpus_filename)
	the_valence_matrix.count_coocs(window_size)
	the_valence_matrix.output_data(output_diretory)
##############################################################################################################################
##############################################################################################################################

main()
