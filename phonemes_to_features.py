import csv

def readInOrthographicalData( \
	input='data/Processed Data with Orthographical Forms - IELEX.csv'):
	"""
	Read in the filtered swadeshed list in the orthographical forms.
	"""
	with open(input) as input_file:
		reader = csv.DictReader(input_file)
		return list(reader)

def readInPhonologicalData( \
	input='data/Processed Data with Phonological Forms - IELEX.csv'):
	"""
	Read in the filtered swadeshed list in the phonological forms.
	"""
	with open(input) as input_file:
		reader = csv.DictReader(input_file)
		return list(reader)

def checkIPASymbols(input, output='output/IPA Symbols - IELEX.txt'):
	"""
	Check the range of IPA symbols of the phonological data.
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

checkIPASymbols(readInPhonologicalData())