import csv

def readInRawData(input='data/Raw Swadesh List Without Url - IELEX.csv'):
	"""
	Read in the raw data.
	:param input: the file name of the input
    :return: the reader of the input file as a list
	"""
	with open(input) as input_file:
		reader = csv.DictReader(input_file)
		return list(reader)

def languagesWithOrthographicForms(raw_input, \
	output='output/Languages with Source Forms.txt'):
	"""
	Return a list of languages that have over 100 words with orthographic forms.
	:param raw_input: the raw input from a reader list
	:param output: the file name of the output
	:return: a sorted list of languages that has 100+ item Swadesh list in orthographic forms
	"""i
	languages_with_orthographic_forms = {}
	for item in raw_input:
		if item['word_orthographic_form'] == '':
			continue
		if '[Legacy]' in item['language_name']:
			continue
		if item['language_name'] not in languages_with_orthographic_forms:
			languages_with_orthographic_forms[item['language_name']] = 1
		else:
			languages_with_orthographic_forms[item['language_name']] += 1
		
	with open(output, "w") as output_file:
		output_file.write("Language: Number of words with orthographic forms\n\n")
		sorted_languages = sorted(languages_with_orthographic_forms.keys())
		for language in sorted_languages:
			if languages_with_orthographic_forms[language] > 100:
				output_file.write("{} {}\n".format(language, \
					languages_with_orthographic_forms[language]))
		return sorted_languages

def languagesWithPhonologicalForms(raw_input, \
	output='output/Languages with Phonological Forms.txt'):
	"""
	Return a list of languages that have over 100 words with phonological forms.
	:param raw_input: the raw input from a reader list
	:param output: the file name of the output
	:return: a sorted list of languages that has 100+ item Swadesh list in phonological forms
	"""
	languages_with_phonological_forms = {}
	for item in raw_input:
		if item['word_phonological_form'] == '' or item['word_phonological_form'] == 'XXX':
			continue
		#if '[Legacy]' in item['language_name']:
		#	continue
		if item['language_name'] not in languages_with_phonological_forms:
			languages_with_phonological_forms[item['language_name']] = 1
		else:
			languages_with_phonological_forms[item['language_name']] += 1
		
	with open(output, "w") as output_file:
		output_file.write("Language: Number of words with phonological forms\n\n")
		languages = []
		for language in sorted(languages_with_phonological_forms.keys()):
			if languages_with_phonological_forms[language] > 100:
				languages += [language]
				output_file.write("{} {}\n".format(language, \
					languages_with_phonological_forms[language]))
		return languages

def generateOrthgraphicSwadeshList(raw_input, languages_orthographic, \
	output='data/Processed Data with Orthographic Forms - IELEX.csv'):
	"""
	Generate a swadesh of orthographic forms for each language that has 100+ 
	words in orthographic forms.
	:param raw_input: the raw input from a reader list
	:param languages_orphographic: a sorted list of languages that has 100+ item 
								   Swadesh list in orthographic forms
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
			if item['language_name'] not in languages_orthographic \
			or item['word_orthographic_form'] == '':
				continue
			writer.writerow({field: item[field] for field in fieldnames})

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


#raw_input = readInRawData()
#languages_orthographic = languagesWithOrthographicForms(raw_input)
#languages_phonological = languagesWithPhonologicalForms(raw_input)
#generateOrthgraphicSwadeshList(raw_input, languages_orthographic)
#generatePhonologicalSwadeshList(raw_input, languages_phonological)
