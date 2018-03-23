import csv
from phonemes_to_features import readInPhonologicalData

def readInRawData(input='data/Geographical Info - ASJP.csv'):
	"""
	Read in the raw data.
	:param input: the file name of the input
    :return: the reader of the input file as a list
	"""
	with open(input) as input_file:
		reader = csv.DictReader(input_file)
		return list(reader)

def generateLongitudeLatitude(raw_input, languages=[]):
	"""
	Generate longitude and latitude infomation of languages.
	:param raw_input: the csv reader of the geographical info
	:param languages: the languages whose longitude and latitude are generated
	:return: a dictionary whose key is the language name and value is pair (longitude, latitude)
	"""
	long_lat = {}
	for item in raw_input:
		if len(languages) == 0:
			long_lat[item['properties/language/name']] = \
				(float(item['properties/language/longitude']),\
				 float(item['properties/language/latitude']))
		else:
			if item['properties/language/name'] in languages:
				long_lat[item['properties/language/name']] = \
					(float(item['properties/language/longitude']),\
					 float(item['properties/language/latitude']))
	return long_lat

def languagesPhonological():
	"""
	Generate a list of languages corresponding to the phonological data
	:return: a set of language names
	"""
	input = readInPhonologicalData()
	languages = set([item['language_name'] for item in input])
	return languages

def writeLongitudeLatitude(output, languages=[]):
	"""
	Write longitude and latitude of languages
	:param languages: the languages whose longitude and latitude are generated
	:param output: name of the output file
	"""
	with open(output, 'w') as output_file:
		fieldnames=['language', 'longitude', 'latitude']
		writer = csv.DictWriter(output_file, fieldnames=fieldnames)
		writer.writeheader()
		long_lat = generateLongitudeLatitude(readInRawData(),languages)
		if len(languages) == 0:
			for language in long_lat:
				(long, lat) = long_lat[language]
				writer.writerow({fieldnames[0]: language, fieldnames[1]: long, fieldnames[2]: lat})
		else:
			for language in languages:
				if language in long_lat:
					(long, lat) = long_lat[language]
					writer.writerow({fieldnames[0]: language, fieldnames[1]: long, fieldnames[2]: lat})
				else:
					writer.writerow({fieldnames[0]:language})

#writeLongitudeLatitude('data/Processed Geographical Info - ASJP.csv')
#writeLongitudeLatitude('output/Geographical Longitude Latitude - ASJP.csv', languagesPhonological())