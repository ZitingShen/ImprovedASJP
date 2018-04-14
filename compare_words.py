#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from phon_util import ipa_symbols, ipa_diacritics_replace, ipa_diacritics_modify, \
					  ipa_joining_bars, ipa_delimiters, feature_saliences, operation_costs
from phonemes_to_features import Word

class WordComparer():
	def __init__(self, word1, word2):
		"""
		Initialize the WordComparer between word1 and word2.
		:param word1: word1 should be the type of Word defined in phonemes_to_features
		:param word2: word2 should be the type of Word defined in phonemes_to_features
		"""
		self.word1 = word1
		self.word2 = word2
		#self.word1 = Word(None, None, word1, set([]))
		#self.word2 = Word(None, None, word2, set([]))
		self.phonemes1 = self.word1.features[self.word1.words[0]]
		self.phonemes2 = self.word2.features[self.word2.words[0]]
		self.matrix = [[0 for j in xrange(len(self.phonemes2)+1)] for i in xrange(len(self.phonemes1)+1)]

	def generate_matrix(self):
		"""
		Generate the modified ALINE similarity matrix between word1 and word2.
		:return: the right bottom value in the matrix, which is the total similarity between word1 and word2
		"""
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
		return self.matrix[-1][-1]

	def print_matrix(self):
		"""
		Print the similarity matrix between word1 and word2.
		:return: void
		"""
		print self.matrix

	def skip(self):
		"""
		:return: the operation cost of skipping a phoneme
		"""
		return operation_costs['skip']

	def substitute(self, phoneme1, phoneme2):
		"""
		:param phoneme1: the phoneme being swapped out
		:param phoneme2: the phoneme being swapped in
		:return: the operation cost of substituting phoneme1 for phoneme2
		"""
		result = operation_costs['substitute']
		for feature in phoneme1.keys():
			if feature in phoneme2:
				result  = result - abs(phoneme1[feature]-phoneme2[feature])*feature_saliences[feature]
		return result

	def expand(self, phoneme1, phoneme2, phoneme3):
		"""
		:param phoneme1: the phoneme being expanded
		:param phoneme2: one of the phonemes being expanded to
		:param phoneme3: the other phoneme being expanded to
		:return: the operation cost of expanding phoneme1 to phoneme2 and phoneme3
		"""
		result = operation_costs['expand']
		for feature in phoneme1.keys():
			if feature in phoneme2 and feature in phoneme3:
				result  = result - abs(phoneme1[feature]-phoneme2[feature])*feature_saliences[feature] \
								 - abs(phoneme1[feature]-phoneme3[feature])*feature_saliences[feature]
		return result

if __name__ == '__main__':	
	word_comparer = WordComparer('bɑnd', 'bæt')
	print word_comparer.generate_matrix()
	word_comparer.print_matrix()