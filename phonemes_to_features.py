#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import csv
from phon_util import ipa_symbols, ipa_diacritics_replace, ipa_diacritics_modify, ipa_joining_bar

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
		self.features, other_symbols = self.getFeatures()

	def getFeatures(self):
		"""
		Convert the representation to features.
		:return: a list of features corresponding to the representation
		:return: a list of symbols not in the encodings
		"""
		representation_utf8 = self.representation.decode('utf-8')
		features = []
		other_symbols = []
		i = 0
		while i in range(len(representation_utf8)):
			char = representation_utf8[i]
			if char in ipa_symbols:
				features += [ipa_symbols[char].copy()]
			elif char in ipa_diacritics_replace:
				if len(features) > 0:
					features[-1][ipa_diacritics_replace[char][0]] = ipa_diacritics_replace[char][1]
			elif char in ipa_diacritics_modify:
				if len(features) > 0:
					features[-1][ipa_diacritics_modify[char][0]] += ipa_diacritics_modify[char][1]
			elif char in ipa_joining_bar:
				next_char = representation_utf8[i+1]
				if next_char in ipa_symbols:
					next_char_features = ipa_symbols[next_char]
					for feature in features[-1].keys():
						features[-1][feature] = (features[-1][feature] + next_char_features[feature])/2
				else:
					next_char_features = ipa_diacritics_replace[next_char]
					features[-1][next_char_features[0]] = next_char_features[1]
				i += 1
			else:
				other_symbols += [char]
			i += 1
		return features, other_symbols

	def __repr__(self):
		"""
		A string representation of the word.
		:return: the string representation of the word
		"""
		repr = 'Language: ' + self.language + '\n'
		repr += 'Meaning: ' + self.meaning + '\n'
		repr += 'Representation: ' + self.representation + '\n'
		repr += 'Features: ' + '\n'
		for phoneme in self.features:
			repr += '\n'
			for feature in sorted(phoneme.keys()):
				repr += feature + ': ' + str(phoneme[feature]) + '\n'
		return repr

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

def convertToFeatures(input, output='output/Swadesh List as Features.txt'):
	"""
	Check the range of IPA symbols of the phonological data.
	:param input: the reader of the input file as a list
	:param output: the file name of the output
	:return: a list of all words in the data which are represented as features
	"""
	words = [Word(item['language_name'], item['word_meaning'], item['word_phonological_form']) for item in input]

	with open(output, 'w') as output_file:
		output_file.write('Words in Swadesh List as Features\n\n')
		for word in words:
			output_file.write('{}\n'.format(word))
			output_file.write('-'*79)
	return words

#w = Word('some language', 'some meaning', 'herpetón')
#print w
convertToFeatures(readInPhonologicalData())