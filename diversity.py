import csv
from geopy.distance import vincenty
from compare_languages import *

def calculateGeographicalDistance(input='output/Processed Geographical Longitude Latitude - ASJP.csv'):
	long_lat = {}
	diviersities = {}
	with open(input) as input_file:
		reader = csv.DictReader(input_file)
		for row in reader:
			long_lat[row['language']] = (row['longitude'], row['latitude'])

	for language in long_lat:
		diversity = 0.0
		for other_language in long_lat:
			if language == other_language:
				continue
			ling_dist = compare_languages(language, other_language)
			geo_dist = vincenty(long_lat[language], long_lat[other_language]).km
			if geo_dist == 0:
				geo_dist = 100
			print str(ling_dist) + '\t' + str(geo_dist)
			diversity = diversity + ling_dist/geo_dist
		diviersities[language] = diversity

	for key, value in sorted(diviersities.iteritems(), key=lambda (k,v): (v,k)):
		print "%s: %s" % (key, value)
			
calculateGeographicalDistance()