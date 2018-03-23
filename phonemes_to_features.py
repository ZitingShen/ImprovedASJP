#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import csv
import re
from phon_util import ipa_symbols, ipa_diacritics_replace, ipa_diacritics_modify, ipa_joining_bars, ipa_delimiters

class Word:
	def __init__(self, language, meaning, representation, other_symbols):
		"""
		:param language: the language of this word
		:param meaning: the meaning of this word
		:param representation: the orthographic or phonological representation
							   of this word
		"""
		self.language = language
		self.meaning = meaning
		self.representation = representation.decode('utf-8')
		self.words = [word.decode('utf-8').strip() for word in re.split(ipa_delimiters, representation)]
		self.features, word_other_symbols = self.getFeatures()
		for symbol in word_other_symbols:
			other_symbols.add(symbol)

	def getFeatures(self):
		"""
		Convert the representation to features.
		:return: a dict of each word's phonetic sequence and their correponding feature list
		:return: a list of symbols not in the encodings
		"""
		features_dict = {}
		other_symbols = []

		for word in self.words:
			features = []
			i = 0
			while i in range(len(word)):
				if word[i] in ipa_symbols:
					features += [ipa_symbols[word[i]].copy()]
				elif word[i] in ipa_diacritics_replace:
					if len(features) > 0:
						features[-1][ipa_diacritics_replace[word[i]][0]] \
							= ipa_diacritics_replace[word[i]][1]
				elif word[i] in ipa_diacritics_modify:
					if len(features) > 0:
						features[-1][ipa_diacritics_modify[word[i]][0]] \
							+= ipa_diacritics_modify[word[i]][1]
				elif word[i] in ipa_joining_bars:
					if word[i+1] in ipa_symbols:
						next_char_features = ipa_symbols[word[i+1]]
						for feature in features[-1].keys():
							features[-1][feature] = (features[-1][feature] \
													+ next_char_features[feature])/2
					else:
						next_char_features = ipa_diacritics_replace[word[i+1]]
						features[-1][next_char_features[0]] = next_char_features[1]
					i += 1
				elif word[i] == '(':
					i += 1
					while i < len(word) and word[i] != ')':
						i += 1
				else:
					other_symbols += [word[i]]
				i += 1
			features_dict[word] = features
		return features_dict, other_symbols

	def __repr__(self):
		"""
		A string representation of the word.
		:return: the string representation of the word
		"""
		repr = 'Language: ' + self.language + '\n'
		repr += 'Meaning: ' + self.meaning + '\n'
		repr += 'Representation: ' + self.representation + '\n'
		for word in sorted(self.features.keys()):
			repr += '\n'+ '*'*20 + '\n'
			repr += 'Word: ' + word + '\n'
			for phoneme in self.features[word]:
				repr += '\n'
				for feature in sorted(phoneme.keys()):
					repr += feature + ': ' + str(phoneme[feature]) + '\n'
		repr += '-'*79
		return repr.encode('utf-8')

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
	other_symbols = set([])
	words = [Word(item['language_name'], item['word_meaning'], \
			      item['word_phonological_form'], other_symbols) for item in input]

	with open(output, 'w') as output_file:
		output_file.write('Words in Swadesh List as Features\n\n')
		for word in words:
			output_file.write('{}\n'.format(word))

	##print len(other_symbols)		
	##for symbol in other_symbols:
	##	print symbol
	return words

#w = Word('some language', 'some meaning', 'herpetón')
#print w
#convertToFeatures(readInPhonologicalData())