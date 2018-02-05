def generatePhonologicalSwadeshList(raw_input, languages_phonological, \
	output='data/Processed Data with Phonological Forms - IELEX.csv'):
	"""
	Generate a swadesh of phonological forms for each language that has 100+ 
	words in phonological forms.
	:param raw_input: the raw input from a reader list
	:param languages_phonological: a sorted list of languages that has 100+ item 
								   Swadesh list in phonological forms
	:param output: the file name of the output
	:return: void
	"""
	with open(output, 'w') as output_file:
		fieldnames = ['language_name', 'language_code', 'lexemes', 'word_id', \
						'word_meaning', 'word_orthographic_form', \
						'word_phonological_form', 'word_gloss', 'word_notes']
		writer = csv.DictWriter(output_file, fieldnames=fieldnames)
		writer.writeheader()

		for item in raw_input:
			if item['language_name'] not in languages_phonological \
			or item['word_phonological_form'] == '' \
			or item['word_phonological_form'] == 'XXX':
				continue
			writer.writerow({field: item[field] for field in fieldnames})