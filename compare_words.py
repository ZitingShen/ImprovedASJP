#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from phon_util import ipa_symbols, ipa_diacritics_replace, ipa_diacritics_modify, \
					  ipa_joining_bars, ipa_delimiters, feature_saliences, operation_costs
from phonemes_to_features import Word

class WordComparer():
	def __init__(self, word1, word2):
		self.word1 = Word(None, None, word1, set([]))
		self.word2 = Word(None, None, word2, set([]))
		self.phonemes1 = self.word1.features[self.word1.words[0]]
		self.phonemes2 = self.word2.features[self.word2.words[0]]
		self.matrix = [[0 for j in xrange(len(self.phonemes2)+1)] for i in xrange(len(self.phonemes1)+1)]

	def generate_matrix(self):
		for i in xrange(len(self.phonemes1)):
			for j in xrange(len(self.phonemes2)):
					self.matrix[i+1][j+1] = max(self.matrix[i][j+1] + self.skip(),\
												self.matrix[i+1][j] + self.skip(),\
												self.matrix[i][j] + self.substitute(self.phonemes1[i], self.phonemes2[j]))
					if i > 0:
						self.matrix[i+1][j+1] = max(self.matrix[i+1][j+1], self.matrix[i-1][j] + self.expand(self.phonemes2[j], \
													self.phonemes1[i-1], self.phonemes1[i]))
					if j > 0:
						self.matrix[i+1][j+1] = max(self.matrix[i+1][j+1], self.matrix[i][j-1] + self.expand(self.phonemes1[i], \
													self.phonemes2[j-1], self.phonemes2[j]))
		print self.matrix
		return self.matrix[-1][-1]

	def skip(self):
		return operation_costs['skip']

	def substitute(self, phoneme1, phoneme2):
		result = operation_costs['substitute']
		for feature in phoneme1.keys():
			if feature in phoneme2:
				result  = result - abs(phoneme1[feature]-phoneme2[feature])*feature_saliences[feature]
		return result

	def expand(self, phoneme1, phoneme2, phoneme3):
		result = operation_costs['expand']
		for feature in phoneme1.keys():
			if feature in phoneme2 and feature in phoneme3:
				result  = result - abs(phoneme1[feature]-phoneme2[feature])*feature_saliences[feature] \
								 - abs(phoneme1[feature]-phoneme3[feature])*feature_saliences[feature]
		return result

word_comparer = WordComparer('\'na:mə', '\'imʲa')
print word_comparer.generate_matrix()