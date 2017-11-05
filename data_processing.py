import csv

def readInRawData(input='data/Raw Swadesh List Without Url - IELEX.csv'):
	"""
	Read in the raw data.
	"""
	with open(input) as input_file:
		reader = csv.DictReader(input_file)
		return list(reader)

def languagesWithOrthographicForms(raw_input, \
	output='output/Languages with Source Forms.txt'):
	"""
	Return a list of languages that have over 100 words with orthographical forms.
	"""
	languages_with_orthographical_forms = {}
	for item in raw_input:
		if item['word_orthographical_form'] == '':
			continue
		if '[Legacy]' in item['language_name']:
			continue
		if item['language_name'] not in languages_with_orthographical_forms:
			languages_with_orthographical_forms[item['language_name']] = 1
		else:
			languages_with_orthographical_forms[item['language_name']] += 1
		
	with open(output, "w") as output_file:
		output_file.write("Language: Number of words with orthographical forms\n\n")
		sorted_languages = sorted(languages_with_orthographical_forms.keys())
		for language in sorted_languages:
			if languages_with_orthographical_forms[language] > 100:
				output_file.write("{}: {}\n".format(language, \
					languages_with_orthographical_forms[language]))
		return sorted_languages

def languagesWithPhonologicalForms(raw_input, \
	output='output/Languages with phonological Forms.txt'):
	"""
	Return a list of languages that have over 100 words with phonological forms.
	"""
	languages_with_phonological_forms = {}
	for item in raw_input:
		if item['word_phonological_form'] == '':
			continue
		if '[Legacy]' in item['language_name']:
			continue
		if item['language_name'] not in languages_with_phonological_forms:
			languages_with_phonological_forms[item['language_name']] = 1
		else:
			languages_with_phonological_forms[item['language_name']] += 1
		
	with open(output, "w") as output_file:
		output_file.write("Language: Number of words with phonological forms\n\n")
		sorted_languages = sorted(languages_with_phonological_forms.keys())
		for language in sorted_languages:
			if languages_with_phonological_forms[language] > 100:
				output_file.write("{}: {}\n".format(language, \
					languages_with_phonological_forms[language]))
		return sorted_languages

def generateOrthgraphicSwadeshList(raw_input, languages_orthographical, \
	output='data/Processed Data with Orthograhic Forms - IELEX.csv'):
	"""
	Generate a swadesh of orthographical forms for each language that has 100+ 
	words in orthographical forms.
	"""
	with open(output, 'w') as output_file:
		fieldnames = ['language_name', 'language_code', 'lexemes', 'word_id', \
						'word_meaing', 'word_orthographical_form', \
						'word_phonological_form', 'word_gloss', 'word_notes']
		writer = csv.DictWriter(output_file, fieldnames=fieldnames)
		writer.writeheader()

		for item in raw_input:
			if item['language_name'] not in languages_orthographical \
			or item['word_orthographical_form'] == '':
				continue
			writer.writerow({field: item[field] for field in fieldnames})

def generatePhonologicalSwadeshList(raw_input, languages_phonological, \
	output='data/Processed Data with Phonological Forms - IELEX.csv'):
	"""
	Generate a swadesh of phonological forms for each language that has 100+ 
	words in phonological forms.
	"""
	with open(output, 'w') as output_file:
		fieldnames = ['language_name', 'language_code', 'lexemes', 'word_id', \
						'word_meaing', 'word_orthographical_form', \
						'word_phonological_form', 'word_gloss', 'word_notes']
		writer = csv.DictWriter(output_file, fieldnames=fieldnames)
		writer.writeheader()

		for item in raw_input:
			if item['language_name'] not in languages_phonological \
			or item['word_phonological_form'] == '':
				continue
			writer.writerow({field: item[field] for field in fieldnames})


raw_input = readInRawData()
languages_orthographical = languagesWithOrthographicForms(raw_input)
languages_phonological = languagesWithPhonologicalForms(raw_input)
generateOrthgraphicSwadeshList(raw_input, languages_orthographical)
generatePhonologicalSwadeshList(raw_input, languages_phonological)
