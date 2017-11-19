import csv

class Word:
	def __init__(self, language, meaning, representation):
		"""
		:param language: the language of this word
		:param meaning: the meaning of this word
		:param representation: the orthographic or phonological representation
							   of this word
		"""
		self.language = language
		self.meaning = meaning
		self.representation = representation
		self.features = getFeatures(representation)

	def getFeatures(self):
		"""
		Convert the representation to features.
		:return: a list of features corresponding to the representation
		"""
		continue

def readInOrthographicData( \
	input='data/Processed Data with Orthographic Forms - IELEX.csv'):
	"""
	Read in the filtered swadeshed list in the orthographic forms.
	:param input: the file name of the input
	:return: the reader of the input file as a list
	"""
	with open(input) as input_file:
		reader = csv.DictReader(input_file)
		return list(reader)

def readInPhonologicalData( \
	input='data/Processed Data with Phonological Forms - IELEX.csv'):
	"""
	Read in the filtered swadeshed list in the phonological forms.
	:param input: the file name of the input
	:return: the reader of the input file as a list
	"""
	with open(input) as input_file:
		reader = csv.DictReader(input_file)
		return list(reader)

def checkIPASymbols(input, output='output/IPA Symbols - IELEX.txt'):
	"""
	Check the range of IPA symbols of the phonological data.
	:param input: the reader of the input file as a list
	:param output: the file name of the output
	:return: a list of IPA symbols used in the phonological data
	"""
	symbols = {}
	for item in input:
		for char in item['word_phonological_form'].decode('utf-8'):
			symbols[char] = item['word_phonological_form']

	with open(output, 'w') as output_file:
		output_file.write('IPA symbol: Sample usage\n\n')
		for symbol in sorted(symbols):
			output_file.write('{}: {}\n'.format(symbol.encode('utf8'), \
				symbols[symbol]))
	return symbols

