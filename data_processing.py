import csv

def languagesWithPhonologicalForms():
	with open('data/Raw Swadesh List Without Url - IELEX.csv') as input_file:
		reader = csv.DictReader(input_file)
		languages_with_phonological_forms = set(row['language_name'] for row in reader if row['word_phonological_form'] != '')
		
	print languages_with_phonological_forms

languagesWithPhonologicalForms()
