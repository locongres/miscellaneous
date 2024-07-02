""" The translatePo function uses the Revirada API (https://revirada.eu/api_info) to translate the content of an Occitan .po file using the content of a French .po file, or vice versa. You will obtain a new .po file in which all the blank msgstr entries and all the ones with the "fuzzy" flag will be translated. The entries already translated or the ones which have no translations in the reference file will be left as is.
This program takes the following arguments:
- Source language: "fra" for French, "oci" for Languedocian Occitan, "oci_gascon" for Gascon Occitan
- Target language: "fra" for French, "oci" for Languedocian Occitan, "oci_gascon" for Gascon Occitan
- Reference .po file: path to the .po file you want to take the original texts from
- .po file to translate: path to the .po file you want to translate the content of
- .po target file: path to the new .po file you want to write the new translations in
Command: translatePo(source_language, target_language, reference_file, file_to_translate, target_file)
To use this program, you need to ask for an API key from the Revirada administrators and replace the YOUR_API_KEY variable (first line of the function) with your own API key.
This function is distributed with the Apache License 2.0.
"""


import sys
import re
import polib
import requests
import json

def translatePo(sourcelang, targetlang, fichfr, fichoc, fichsort):

	key="YOUR_API_KEY"
	url = "https://api.revirada.eu/translate_string"

	fr = polib.pofile(fichfr)

	translations = {entry.msgid: entry.msgstr for entry in fr}



	oc = polib.pofile(fichoc)

	po = polib.POFile()

	po.metadata = oc.metadata
	po.header = oc.header


	cpt=0
	for entry in oc:
		cpt+=1
		sys.stderr.write('Tractament entrada '+str(cpt)+'/'+str(len(oc))+'...\n')
		
		if not entry.obsolete and entry.msgid!="":
			if entry.msgstr=="" or 'fuzzy' in entry.flags:
				if entry.msgid in translations and translations[entry.msgid]!="":
					tradfr=translations[entry.msgid]
					
					payload = {'api_key': 'df48ab943cb849acbd3766b1491f02e8',
					'engine': 'apertium',
					'content_type': 'html',
					'text': tradfr,
					'source_language': sourcelang,
					'target_language': targetlang}
					files=[

					]
					headers = {}

					response = requests.request("POST", url, headers=headers, data=payload, files=files)
					
					try:
						data = json.loads(response.text)
					except json.JSONDecodeError as e:
						sys.stderr.write(f"Error while parsing JSON response from Revirada API: {e}")
						continue
					
					if "translated_text" in data:
					
						entry.msgstr=data["translated_text"]
						
						if 'fuzzy' in entry.flags:
							# Retirer le flag "fuzzy"
							entry.flags.remove('fuzzy')
			
		po.append(entry)
						
					


	# Écrit le fichier .po
	po.save(fichsort)


