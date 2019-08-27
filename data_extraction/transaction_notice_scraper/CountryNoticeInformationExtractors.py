from TransactionInformationExtractor import TransactionInformationExtractor 				# Implemented Interface
from utility import getCompanyFormPositionsInText, getReadableEntity						# import functions from utility class
from utility import detectlang, translateToEnglish,containsCompanyForm,cleanCompanyName		# import functions from utility class
from utility import is_relevant_notice,find_supersets,preprocessNoticeText					# import functions from utility class
import pycountry																			# pycountry recognize countries in text
from geotext import GeoText		 															# geotext for recognising and differentiating between countries and cities in text
from google.cloud import translate 															# Import translate module from Google Cloud services
import os																					# Operating system specific methods 
import re 																					# Import regular expression string pattern matching library
from staticfields import *																	# Import constant fields
from cleanco import cleanco 																# cleanco library company names extraction
from fuzzywuzzy import fuzz 																# Fuzzy string matching
from fuzzywuzzy import process 																# Fuzzy string matching
import string

# ------------------------------------------------------------------------------------------- #
# ------------------------------------- Class to handle German notices ---------------------- #
# ------------------------------------------------------------------------------------------- #
class GermanyNoticeInformationExtractor(TransactionInformationExtractor):
	# Return english version of notice
	def getEnglishNotice(self):
		return self.englishNoticeText

	# Description: 	Function to obtain a list of entities that could possibly be company names in the piece of text (the candidates)
	# Output:		a list of phrases or words in the text that could be company names (organisations, persons, geopolitical locations and miscellaneous entities)
	def extractPossibleCompanyNames(self):

		nlptask	 		= self.germannlp(self.noticeText)				# construct a german nlp task 
		englishnlptask 		= self.englishnlp(self.englishNoticeText)		# construct an english nlp task 

		possibleCompanyNames = []
		companyFormsAdded = []

		# # First find possible company names in original language text
		# for entity in nlptask.ents:
		# 	if entity.label_ in ['ORG']:
		# 		possibleCompanyNames.append((entity.text,entity.label_))

		# # Add possible company names from translated English text
		# for entity in englishnlptask.ents:
		# 	if entity.label_ in ['ORG']:
		# 		possibleCompanyNames.append((entity.text,entity.label_))

		# Now try to recognize companies by trying to identify company forms in the text
		companyFormsInNotice = getCompanyFormPositionsInText(self.noticeText)
		text = self.noticeText
		for companyForm in companyFormsInNotice:
			cf = companyForm[0]										# String representation of company form
			companyFormsAdded.append(cf.lower())
			cfstart = companyForm[1]								# Start index of company form
			cnstart = cfstart - 35									# Lets assume that the company name starts at most 35 characters
																	# before the start of the company form in the notice text 

			if (cnstart > 0):										# There are at least 35 characters of text preceding the company form
				companyName = text[cnstart:cfstart-1] + " " + cf.lower() 	# add company form
				if ("gmbh" not in companyName.lower()):# and (cf.lower() not in companyFormsAdded):
					possibleCompanyNames.append(cleanCompanyName(companyName))			# add to list of candidate company names
			else:													# There are less than 35 characters to the start of the notice from the company form
				cnstart = 0
				companyName = text[cnstart:cfstart-1] + " " + cf.lower() 	# add company form
				if ("gmbh" not in companyName.lower()):# and (cf.lower() not in companyFormsAdded):
					possibleCompanyNames.append(cleanCompanyName(companyName))			# add to list of candidate company names

		#result = find_supersets(possibleCompanyNames)
		result = list(set(possibleCompanyNames))

		return result

	# Description:	Function to extract countries mentioned in a notice
	# Output: 		a list of countries appearing in the notice
	def extractCandidateCountries(self):
		nlptask	 			= self.germannlp(self.noticeText)				# construct a german nlp task 
		englishnlptask 		= self.englishnlp(self.englishNoticeText)		# construct an english nlp task 
		countries = []

		# First try pycountry
		for country in pycountry.countries:
			if country.name in self.noticeText:
				countries.append(country.alpha_2)

		# try geotext & country code lookup tables

		# first the original language
		for ent in nlptask.ents:
			if (ent.label_ == "GPE"):
				newStr = ent.text.split(".")
				#print(newStr[0])
				tmp = GeoText(newStr[0])
				countries.extend(tmp.country_mentions)
				for k, v in StaticFields.euMemberStates.items():
					for item in v:
						if item == newStr[0]:
							countries.append(k)

		# now try english
		for ent in englishnlptask.ents:
			if (ent.label_ == "GPE"):
				newStr = ent.text.split(".")
				tmp = GeoText(newStr[0])
				countries.extend(tmp.country_mentions)
				for k, v in StaticFields.euMemberStates.items():
					for item in v:
						if item == newStr[0]:
							countries.append(k)
			
		# Remove duplicates
		countries = list(set(countries))
		return countries

	# Description: Function specific for notices from German registry, to extract the non-German companies mentioned in the notice
	# Output: the first non-German EU company mentioned in the notice
	def extractNonGermanCompanyCountry(self):

		nlptask	 			= self.germannlp(self.noticeText)				# construct a german nlp task 
		englishnlptask 		= self.englishnlp(self.englishNoticeText)		# construct an english nlp task 
		countries = []

		# First try pycountry
		for country in pycountry.countries:
			if country.name in self.noticeText:
				countries.append(country.alpha_2)

		# try geotext & country code lookup tables

		# first the original language
		for ent in nlptask.ents:
			if (ent.label_ == "GPE"):
				newStr = ent.text.split(".")
				#print(newStr[0])
				tmp = GeoText(newStr[0])
				countries.extend(tmp.country_mentions)
				for k, v in StaticFields.euMemberStates.items():
					if (k == newStr[0]):
						countries.append(k)
					for item in v:
						if item == newStr[0]:
							countries.append(k)

		# now try english
		for ent in englishnlptask.ents:
			if (ent.label_ == "GPE"):
				newStr = ent.text.split(".")
				tmp = GeoText(newStr[0])
				countries.extend(tmp.country_mentions)
				for k, v in StaticFields.euMemberStates.items():
					if (k == newStr[0]):
						countries.append(k)
					for item in v:
						if item == newStr[0]:
							countries.append(k)
		
		# filter irrelevant
		countries = list(set(countries))
		if 'DE' in countries:
			countries.remove('DE')
		if 'GB' in countries:
			countries.remove('GB')
			countries.append('UK')
		if (len(countries) == 0):
			return "-"
		result = []
		for c in countries:
			for k, v in StaticFields.euMemberStates.items():
				if (k == c):
					result.append(c)
				for item in v:
					if item == c:
						result.append(k)

		result = list(set(result))
		if (len(result) > 0):
			return result[0]
		else:
			return "-"

	# Description: 	Function to extract the registration number of the company involved in the transaction which is NOT from the notice registry country
	# Parameter: 	country from which the company comes from
	# Output: 		registration number of the company
	def extractRegistrationNumber(self, country):
		doc = self.germannlp(self.noticeText)
		doc2 = self.englishnlp(self.englishNoticeText)

		if (country == "UK"): # United Kingdom seven or eight digit number (if it is seven digit the 0 in the beginning is omitted ) (Wales is often mention shortly before the number) 
			for token in doc2:
				nums = re.match(r'^([\s\d]+)$', token.text)
				if nums is not None:
					if (token.pos_ == "NUM" and (len(token.text) == 7 or len(token.text) == 8) and len(token.text) == (nums.end() - nums.start())):
						tmp = token.text
						if (len(tmp) == 8 and (tmp[0] == "0" or tmp[0] == "1")):
							return tmp
						elif (len(tmp) == 7 and tmp[0] != "0"):
							return "0"+tmp

		elif (country == "LU"): # Luxemburg B followed by a six digit number 
			for token in doc2:
				nums = re.match(r'^([\s\d]+)$', token.text)
				if nums is not None:
					if (token.pos_ == "NUM" and (len(token.text) == 6) and len(token.text) == (nums.end() - nums.start())):
						return "B"+token.text

			p = re.findall(r'(\d{6})', self.noticeText)

			if (len(p) > 0):
				for item in p:
					idx = self.noticeText.find(item)
					if ((self.noticeText[idx-4] != "H" or self.noticeText[idx-3] != "R" or self.noticeText[idx-2] != "B") and (self.noticeText[idx-3] != "H" or self.noticeText[idx-2] != "R" or self.noticeText[idx-1] != "B")):
						return "B"+item

		elif (country == "BE"): # Belgium a nine digit number separated by coma a dot each three digits i.e. abc123.456mno.789xyz
			for token in doc2:
				if (token.pos_ == "NUM" and (len(token.text) >= 11 and len(token.text) <= 12) and ("." in token.text)):
					tmp = token.text
					parts = tmp.split(".")
					if len(parts) >= 3:
						if ((len(parts[0]) == 3 or len(parts[0]) == 4) and (len(parts[1]) == 3 and len(parts[2]) == 3)):
							return tmp

		elif ((country == "NL") or (country == "EE") or (country == "DK") or (country == "SK")): # Denmark, Estonia, Netherlands, Slovakia 8 digit number
			for token in doc2:
				nums = re.match(r'^([\s\d]+)$', token.text)
				if nums is not None:
					if (token.pos_ == "NUM" and (len(token.text) == 8) and len(token.text) == (nums.end() - nums.start())):
						return token.text

			p = re.findall(r'(\d{8})', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

		elif (country == "LV"): # Latvia 11 digit number
			for token in doc2:
				nums = re.match(r'^([\s\d]+)$', token.text)
				if nums is not None:
					if (token.pos_ == "NUM" and (len(token.text) == 11) and len(token.text) == (nums.end() - nums.start())):
						return token.text
		
			p = re.findall(r'(\d{11})', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

		elif (country == "MT"): # Malta 5 digit number
			for token in doc2:
				nums = re.match(r'^([\s\d]+)$', token.text)
				if nums is not None:
					if (token.pos_ == "NUM" and (len(token.text) == 5) and len(token.text) == (nums.end() - nums.start())):
						return token.text
		
			p = re.findall(r'(\d{5})', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

		elif (country == "PL") or (country == "SI"): # Poland and Slovenia 10 digit number
			for token in doc2:
				nums = re.match(r'^([\s\d]+)$', token.text)
				if nums is not None:
					if (token.pos_ == "NUM" and (len(token.text) == 10) and len(token.text) == (nums.end() - nums.start())):
						return token.text
		
			p = re.findall(r'(\d{10})', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

		elif (country == "FI"): # Finland 7 digit number followed by -digit-
			p = re.findall(r'(\d{7})-\d{1}-', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

		elif (country == "IT"): # Italy 11 digit number OR two letters of city + 7 digit number
			p = re.findall(r'(\d{11})', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

			p = re.findall(r'[a-zA-Z]{2}[\s?]{0,1}[0-9]{7}$', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

		elif (country == "HU"): # Hungary 10 digit number formatted as follows: 2 digits-2 digits-6 digits
			p = re.findall(r'(\d{2})-\d{2}-\d{6} ', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

		elif (country == "SE"): # Sweden 10 digits like 6 digits-4 digits
			p = re.findall(r'\d{6}-\d{4}', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

		elif (country == "RO"): # J40/8302/1997 (registration number) or fiscal code (12751583)
			p = re.findall(r'\s+[A-Z]\d{2}/\d{4}/\d{4}\s+', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

			p = re.findall(r'(\d{8})', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

		elif ((country == "HR") or (country == "FR") or (country == "BG") or (country == "LT") or (country == "PT")): # Croatia, France, Lithuania, Portugal, Bulgaria 9 digit number
			for token in doc2:
				nums = re.match(r'^([\s\d]+)$', token.text)
				if nums is not None:
					if (token.pos_ == "NUM" and (len(token.text) == 9) and len(token.text) == (nums.end() - nums.start())):
						return token.text
		
			p = re.findall(r'(\d{9})', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

		elif ((country == "CY") or (country == "IE") or (country == "GR")): # Cyprus, Ireland, Greece 6 digit number
			for token in doc2:
				nums = re.match(r'^([\s\d]+)$', token.text)
				if nums is not None:
					if (token.pos_ == "NUM" and (len(token.text) == 6) and len(token.text) == (nums.end() - nums.start())):
						return token.text
		
			p = re.findall(r'(\d{6})', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

		elif (country == "AT"): # FN followed by a 6 digit number and a letter (e.g. FN 123456a) sometimes found as Fachbuch Nummer
			for token in doc2:
				nums = re.match(r'^([\s\d]+)$', token.text)
				if nums is not None:
					if (token.pos_ == "NUM" and (len(token.text) == 6) and len(token.text) == (nums.end() - nums.start())):
						idx = self.noticeText.find(token.text)
						if ((self.noticeText[idx-3] == "F" and self.noticeText[idx-2] == "N") or (self.noticeText[idx-2] == "F" and self.noticeText[idx-1] == "N")):
							idx2 = idx + len(token.text)
							test = ""
							if self.noticeText[idx2] == " ":
								test = test + self.noticeText[idx2+1]
							else:
								test = test + self.noticeText[idx2]

							if (test.isalpha()):
								return "FN"+token.text+test
							else:
								return "FN"+token.text
						elif ((self.noticeText[idx-4] != "H" or self.noticeText[idx-3] != "R" or self.noticeText[idx-2] != "B") and (self.noticeText[idx-3] != "H" or self.noticeText[idx-2] != "R" or self.noticeText[idx-1] != "B")):
							return token.text

			p = re.findall(r'(\d{6})', self.noticeText)
			if (len(p) > 0):
				for item in p:
					idx = self.noticeText.find(item)
					if ((self.noticeText[idx-4] != "H" or self.noticeText[idx-3] != "R" or self.noticeText[idx-2] != "B") and (self.noticeText[idx-3] != "H" or self.noticeText[idx-2] != "R" or self.noticeText[idx-1] != "B")):
						return "FN"+item

		elif (country == "ES"): # Spain any 5 to 9 digit number
			p = re.findall(r'[a-zA-Z]{1}[\s?]{0,1}[0-9]{5,9}$', self.englishNoticeText)
			if (len(p) > 0):
				return p[0]

		elif (country == "CZ"): # Czech Republic 9 digit number
			for token in doc2:
				nums = re.match(r'^([\s\d]+)$', token.text)
				if nums is not None:
					if (token.pos_ == "NUM" and (len(token.text) == 9) and len(token.text) == (nums.end() - nums.start())):
						return token.text
			
			p = re.findall(r'(\d{9})', self.englishNoticeText)
			
			if (len(p) > 0):
				return p[0]
		else:
			return []

	# Description: 	Function to extract the registration number of the company involved in the transaction which is NOT from the notice registry country
	# Parameter: 	list of possible countries appearing in the notice
	# Output: 		registration number of the company
	def extractCandidateRegNumbers(self, countries):
		doc = self.germannlp(self.noticeText)
		doc2 = self.englishnlp(self.englishNoticeText)
		result = []
		for country in countries:
			if (country == "UK"): # United Kingdom seven or eight digit number (if it is seven digit the 0 in the beginning is omitted ) (Wales is often mention shortly before the number) 
				for token in doc2:
					nums = re.match(r'^([\s\d]+)$', token.text)
					if nums is not None:
						if (token.pos_ == "NUM" and (len(token.text) == 7 or len(token.text) == 8) and len(token.text) == (nums.end() - nums.start())):
							tmp = token.text
							if (len(tmp) == 8 and (tmp[0] == "0" or tmp[0] == "1")):
								result.append(tmp)
							elif (len(tmp) == 7 and tmp[0] != "0"):
								result.append("0"+tmp)

			elif (country == "LU"): # Luxemburg B followed by a six digit number 
				for token in doc2:
					nums = re.match(r'^([\s\d]+)$', token.text)
					if nums is not None:
						if (token.pos_ == "NUM" and (len(token.text) == 6) and len(token.text) == (nums.end() - nums.start())):
							result.append("B"+token.text)

				p = re.findall(r'(\d{6})', self.noticeText)

				if (len(p) > 0):
					for item in p:
						idx = self.noticeText.find(item)
						if ((self.noticeText[idx-4] != "H" or self.noticeText[idx-3] != "R" or self.noticeText[idx-2] != "B") and (self.noticeText[idx-3] != "H" or self.noticeText[idx-2] != "R" or self.noticeText[idx-1] != "B")):
							result.append("B"+item)

			elif (country == "BE"): # Belgium a nine digit number separated by coma a dot each three digits i.e. abc123.456mno.789xyz
				for token in doc2:
					if (token.pos_ == "NUM" and (len(token.text) >= 11 and len(token.text) <= 12) and ("." in token.text)):
						tmp = token.text
						parts = tmp.split(".")
						if len(parts) >= 3:
							if ((len(parts[0]) == 3 or len(parts[0]) == 4) and (len(parts[1]) == 3 and len(parts[2]) == 3)):
								result.append(tmp)

			elif ((country == "NL") or (country == "EE") or (country == "DK") or (country == "SK")): # Denmark, Estonia, Netherlands, Slovakia 8 digit number
				for token in doc2:
					nums = re.match(r'^([\s\d]+)$', token.text)
					if nums is not None:
						if (token.pos_ == "NUM" and (len(token.text) == 8) and len(token.text) == (nums.end() - nums.start())):
							result.append(token.text)

				p = re.findall(r'(\d{8})', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

			elif (country == "LV"): # Latvia 11 digit number
				for token in doc2:
					nums = re.match(r'^([\s\d]+)$', token.text)
					if nums is not None:
						if (token.pos_ == "NUM" and (len(token.text) == 11) and len(token.text) == (nums.end() - nums.start())):
							result.append(token.text)
			
				p = re.findall(r'(\d{11})', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

			elif (country == "MT"): # Malta 5 digit number
				for token in doc2:
					nums = re.match(r'^([\s\d]+)$', token.text)
					if nums is not None:
						if (token.pos_ == "NUM" and (len(token.text) == 5) and len(token.text) == (nums.end() - nums.start())):
							result.append(token.text)
			
				p = re.findall(r'(\d{5})', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

			elif (country == "PL") or (country == "SI"): # Poland and Slovenia 10 digit number
				for token in doc2:
					nums = re.match(r'^([\s\d]+)$', token.text)
					if nums is not None:
						if (token.pos_ == "NUM" and (len(token.text) == 10) and len(token.text) == (nums.end() - nums.start())):
							result.append(token.text)
			
				p = re.findall(r'(\d{10})', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

			elif (country == "FI"): # Finland 7 digit number followed by -digit-
				p = re.findall(r'(\d{7})-\d{1}-', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

			elif (country == "IT"): # Italy 11 digit number OR two letters of city + 7 digit number
				p = re.findall(r'(\d{11})', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

				p = re.findall(r'[a-zA-Z]{2}[\s?]{0,1}[0-9]{7}$', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

			elif (country == "HU"): # Hungary 10 digit number formatted as follows: 2 digits-2 digits-6 digits
				p = re.findall(r'(\d{2})-\d{2}-\d{6} ', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

			elif (country == "SE"): # Sweden 10 digits like 6 digits-4 digits
				p = re.findall(r'\d{6}-\d{4}', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

			elif (country == "RO"): # J40/8302/1997 (registration number) or fiscal code (12751583)
				p = re.findall(r'\s+[A-Z]\d{2}/\d{4}/\d{4}\s+', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

				p = re.findall(r'(\d{8})', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

			elif ((country == "HR") or (country == "FR") or (country == "BG") or (country == "LT") or (country == "PT")): # Croatia, France, Lithuania, Portugal, Bulgaria 9 digit number
				for token in doc2:
					nums = re.match(r'^([\s\d]+)$', token.text)
					if nums is not None:
						if (token.pos_ == "NUM" and (len(token.text) == 9) and len(token.text) == (nums.end() - nums.start())):
							result.append(token.txt)
			
				p = re.findall(r'(\d{9})', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

			elif ((country == "CY") or (country == "IE") or (country == "GR")): # Cyprus, Ireland, Greece 6 digit number
				for token in doc2:
					nums = re.match(r'^([\s\d]+)$', token.text)
					if nums is not None:
						if (token.pos_ == "NUM" and (len(token.text) == 6) and len(token.text) == (nums.end() - nums.start())):
							result.append(token.txt)
			
				p = re.findall(r'(\d{6})', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

			elif (country == "AT"): # FN followed by a 6 digit number and a letter (e.g. FN 123456a) sometimes found as Fachbuch Nummer
				for token in doc2:
					nums = re.match(r'^([\s\d]+)$', token.text)
					if nums is not None:
						if (token.pos_ == "NUM" and (len(token.text) == 6) and len(token.text) == (nums.end() - nums.start())):
							idx = self.noticeText.find(token.text)
							if ((self.noticeText[idx-3] == "F" and self.noticeText[idx-2] == "N") or (self.noticeText[idx-2] == "F" and self.noticeText[idx-1] == "N")):
								idx2 = idx + len(token.text)
								test = ""
								if self.noticeText[idx2] == " ":
									test = test + self.noticeText[idx2+1]
								else:
									test = test + self.noticeText[idx2]

								if (test.isalpha()):
									result.append("FN"+token.text+test)
								else:
									result.append("FN"+token.text)
							elif ((self.noticeText[idx-4] != "H" or self.noticeText[idx-3] != "R" or self.noticeText[idx-2] != "B") and (self.noticeText[idx-3] != "H" or self.noticeText[idx-2] != "R" or self.noticeText[idx-1] != "B")):
								result.append(token.txt)

				p = re.findall(r'(\d{6})', self.noticeText)
				if (len(p) > 0):
					for item in p:
						idx = self.noticeText.find(item)
						if ((self.noticeText[idx-4] != "H" or self.noticeText[idx-3] != "R" or self.noticeText[idx-2] != "B") and (self.noticeText[idx-3] != "H" or self.noticeText[idx-2] != "R" or self.noticeText[idx-1] != "B")):
							result.append("FN"+item)

			elif (country == "ES"): # Spain any 5 to 9 digit number
				p = re.findall(r'[a-zA-Z]{1}[\s?]{0,1}[0-9]{5,9}$', self.englishNoticeText)
				if (len(p) > 0):
					result.append(p[0])

			elif (country == "CZ"): # Czech Republic 9 digit number
				for token in doc2:
					nums = re.match(r'^([\s\d]+)$', token.text)
					if nums is not None:
						if (token.pos_ == "NUM" and (len(token.text) == 9) and len(token.text) == (nums.end() - nums.start())):
							result.append(token.txt)
				
				p = re.findall(r'(\d{9})', self.englishNoticeText)
				
				if (len(p) > 0):
					result.append(p[0])
			else:
				pass

		return result

	# Function to extract the non-German company from the text (currently working 37/43 correct)
	def extractNonGermanCompany(self,germanCompany):

		text1 = preprocessNoticeText(self.noticeText)
		text2 = preprocessNoticeText(self.englishNoticeText)

		possibleCompanyNames = []
		german_notice = text1
		english_notice = text2
		words1 = german_notice.split(" ")
		words2 = english_notice.split(" ")
		germannlptask = self.germannlp(german_notice)
		englishnlptask = self.englishnlp(english_notice)

		# First try German text
		for ent in germannlptask.ents:
			if (ent.label_ == "ORG" or ent.label_ == "PERSON" or ent.label_ == "GPE"):
				x = cleanco(ent.text)
				nm = x.clean_name() 
				if containsCompanyForm(nm):
					possibleCompanyNames.append(cleanCompanyName(ent.text))
				typ = x.type()
				if typ is None:
					pass
				else:
					nm = x.clean_name() 
					places = GeoText(nm)
					if (len(places.countries) == 1 or len(places.cities) == 1):
						chunks = ent.text.split(" ")
						strtxt = str(ent.text)
						strtxt = words1[words1.index(chunks[0])-1] + " " + strtxt
						possibleCompanyNames.append(cleanCompanyName(strtxt))
					else:
						possibleCompanyNames.append(cleanCompanyName(ent.text))

		# if "Seniorenzentrum" in self.noticeText or "Pareto" in self.noticeText or "FE Industrial" in self.noticeText or "FE Industrial" in self.noticeText or "PRODYNA" in self.noticeText or "Slyman" in self.noticeText:
		# 	print()
		# 	print("German:")
		# 	print(list(set(possibleCompanyNames)))
		# 	print()

		# Then try the English text
		for ent in englishnlptask.ents:
			if (ent.label_ == "ORG" or ent.label_ == "PERSON" or ent.label_ == "GPE"):  
				x = cleanco(ent.text)
				nm = x.clean_name() 
				if containsCompanyForm(nm):
					possibleCompanyNames.append(cleanCompanyName(ent.text))
				# typ = x.type()
				# if typ is None:
				# 	pass
				# else:
				# 	nm = x.clean_name() 
				# 	places = GeoText(nm)
				# 	if (len(places.countries) == 1 or len(places.cities) == 1):
				# 		chunks = ent.text.split(" ")
				# 		print(chunks)
				# 		strtxt = str(ent.text)
				# 		strtxt = words2[words2.index(chunks[0].strip(string.punctuation))-1] + " " + strtxt
				# 		possibleCompanyNames.append(cleanCompanyName(strtxt))
				# 	else:
				# 		possibleCompanyNames.append(cleanCompanyName(ent.text))

		possibleCompanyNames.append(cleanCompanyName(germanCompany))
		possibleCompanyNames = find_supersets(possibleCompanyNames)
		possibleCompanyNames = list(set(possibleCompanyNames))

		# if "Seniorenzentrum" in self.noticeText or "Pareto" in self.noticeText or "FE Industrial" in self.noticeText or "FE Industrial" in self.noticeText or "PRODYNA" in self.noticeText or "Slyman" in self.noticeText:
		# 	print()
		# 	print("English:")
		# 	print(list(set(possibleCompanyNames)))
		# 	print()

		country = self.extractNonGermanCompanyCountry()

		newPossibleCompanyNames = []
		
		if (country != 'AT' and country != 'LV'):
			for item in possibleCompanyNames:
				if "GmbH" not in item and "G mbH" not in item and "Gesellschaft mbH" not in item:
					newPossibleCompanyNames.append(item)
		else:
			newPossibleCompanyNames.extend(possibleCompanyNames)

		if (len(newPossibleCompanyNames) == 0):
			pair = []
			pair.append(text2)
			pair.append("-")
			return pair[1]

		resultCompanies = []
		for item in newPossibleCompanyNames:
			germanCompany = cleanCompanyName(germanCompany)
			tmpCompany = cleanCompanyName(item)
			if (germanCompany != tmpCompany):
				resultCompanies.append(tmpCompany)

		return list(set(resultCompanies))

	# Description: Function to get the type of an individual notice (CBM, ST or SE)
	# Output:   "CBM" if the type of transaction described in the notice is a cross-border merger (CBM)
	# Output:   "ST" if the type of transaction described in the notice is a seat transfer (ST)
	# Output:   "SE" if the type of transaction described in the notice is a Societas Europa (SE), which is a special type of CBM
	def getNoticeType(self):
		# Initialise flags for different types of transaction
		possiblyCBM = False
		possiblyST = False
		possiblySE = False

		# Check if it is a CBM
		if (is_relevant_notice(self.noticeText, StaticFields.cbm_kw_1, 'and') or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_2, 'and') 
			or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_3, 'and') or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_4, 'and') 
			or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_5, 'and') or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_6, 'and')
			or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_7, 'and') or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_8, 'and')
			or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_9, 'and') or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_10, 'and')
			or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_11, 'and') or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_12, 'and')
			or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_13, 'and') or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_14, 'and')
			or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_15, 'and') or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_16, 'and')
			or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_17, 'and') or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_18, 'and')
			or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_19, 'and') or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_20, 'and')
			or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_21, 'and') or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_22, 'and')
			or is_relevant_notice(self.noticeText, StaticFields.cbm_kw_23, 'and')):
			# Make sure this word is not in the text
			if (StaticFields.cbm_kw_NOT[0] in self.noticeText):
				pass
			else:
				possiblyCBM = True

		# Check if it is an ST
		if (is_relevant_notice(self.noticeText, StaticFields.st_kw_1, 'and') or is_relevant_notice(self.noticeText, StaticFields.st_kw_2, 'and')
			or is_relevant_notice(self.noticeText, StaticFields.st_kw_3, 'and') or is_relevant_notice(self.noticeText, StaticFields.st_kw_4, 'and')
			or is_relevant_notice(self.noticeText, StaticFields.st_kw_5, 'and')):
			# Make sure these phrases are not in the text
			if ("grenzuberschreitende verschmelzung" in getReadableEntity(self.noticeText.lower()) or "grenzuberschreitenden verschmelzung" in getReadableEntity(self.noticeText.lower())
				or StaticFields.st_kw_NOT[0] in self.noticeText or StaticFields.st_kw_NOT[1] in self.noticeText
				or StaticFields.st_kw_NOT2[0] in self.noticeText or StaticFields.st_kw_NOT[1] in self.noticeText):
				pass
			else:
				possiblyST = True

		# Check if it is an SE
		if (is_relevant_notice(self.noticeText, StaticFields.se_kw_1, 'and') or is_relevant_notice(self.noticeText, StaticFields.se_kw_2, 'and') or is_relevant_notice(self.noticeText, StaticFields.se_kw_3, 'and') or is_relevant_notice(self.noticeText, StaticFields.se_kw_4, 'and')):
			if possiblyST and possiblyCBM:
				possiblySE = True
				# Make sure these phrases are not in the text
			if ("grenzuberschreitende verschmelzung" in getReadableEntity(self.noticeText.lower()) or "grenzuberschreitenden verschmelzung" in getReadableEntity(self.noticeText.lower())):
				possiblySE = True

		if possiblyST:
			return "ST"

		if possiblyCBM:
			if possiblySE:
				return "SE"
			return "CBM"
		
		return "UNKNOWN"

# ------------------------------------------------------------------------------------------- #
# ------------------------------------- END: GermanNoticeInformationExtractor --------------- #
# ------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------------------- #
# ------------------------------------- Class to handle French notices ---------------------- #
# ------------------------------------------------------------------------------------------- #
class LuxembourgNoticeInformationExtractor(TransactionInformationExtractor):
	# Return english version of notice
	def getEnglishNotice(self):
		return self.englishNoticeText

	def getName(self):
		return "Luxembourg"

	# Description: 	Function to obtain a list of entities that could possibly be company names in the piece of text (the candidates)
	# Output:		a list of phrases or words in the text that could be company names (organisations, persons, geopolitical locations and miscellaneous entities)
	def extractPossibleCompanyNames(self):
		nlptask = self.englishnlp(self.englishNoticeText)		# construct an english nlp task 
		if (self.language == 'fr'):
			nlptask	 = self.frenchnlp(self.noticeText)				# construct a french nlp task 
		elif (self.language == 'de'):
			nlptask	 = self.germannlp(self.noticeText)				# construct a german nlp task 	

		possibleCompanyNames =[]

		# # First find possible company names in original language text
		# for entity in nlptask.ents:
		# 	if entity.label_ in ['ORG']:
		# 		possibleCompanyNames.append((entity.text,entity.label_))

		# # Add possible company names from translated English text
		# for entity in englishnlptask.ents:
		# 	if entity.label_ in ['ORG']:
		# 		possibleCompanyNames.append((entity.text,entity.label_))

		# Now try to recognize companies by trying to identify company forms in the text
		companyFormsInNotice = getCompanyFormPositionsInText(self.noticeText)
		text = self.noticeText
		for companyForm in companyFormsInNotice:
			cf = companyForm[0]										# String representation of company form
			cfstart = companyForm[1]								# Start index of company form
			cnstart = cfstart - 35									# Lets assume that the company name starts at most 35 characters
																	# before the start of the company form in the notice text 

			if (cnstart > 0):										# There are at least 35 characters of text preceding the company form
				companyName = text[cnstart:cfstart-1] + " " + cf 	# add company form
				possibleCompanyNames.append(companyName)			# add to list of candidate company names
			else:													# There are less than 35 characters to the start of the notice from the company form
				cnstart = 0
				companyName = text[cnstart:cfstart-1] + " " + cf 	# add company form
				possibleCompanyNames.append(conmpanyName)			# add to list of candidate company names

		result = find_supersets(possibleCompanyNames)
		# Remove duplicates
		return result#list(set(possibleCompanyNames))

	def extractCandidateCountries(self):
		return "Luxembourg"

	def extractRegistrationNumber(self):
		return "007"

	def getNoticeType(self):
		transactionType = "-"
		if "projet de fusion" in self.noticeText.lower():
			transactionType = "CBM"
		if "scission" in self.noticeText.lower():
			transactionType = "CBD"
		if "transfert de patrimoine" in self.noticeText.lower() or "transfert de branche d'activité" in self.noticeText.lower() or "transfert de d'actifs" in self.noticeText.lower():
			transactionType = "ST"
		return transactionType

	def extractCandidateRegNumbers(self,countries):
		return "CBM"
		
# ------------------------------------------------------------------------------------------- #
# ------------------------------------- END: FrenchNoticeInformationExtractor --------------- #
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# ------------------------------------- Class to handle English notices --------------------- #
# ------------------------------------------------------------------------------------------- #
class UKNoticeInformationExtractor(TransactionInformationExtractor):
	
	def getName(self):
		return "UK"

	def extractPossibleCompanyNames(self):
		return self.noticeText + self.getName()

	def extractCandidateCountries(self):
		return "UK"

	def extractRegistrationNumber(self):
		return "008"

	def getNoticeType(self):
		return "CBM"

	def extractCandidateRegNumbers(self,countries):
		return "CBM"

# ------------------------------------------------------------------------------------------- #
# ------------------------------------- END: EnglishNoticeInformationExtractor -------------- #
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# ------------------------------------- Class to handle Dutch notices --------------------- #
# ------------------------------------------------------------------------------------------- #

class BelgiumNoticeInformationExtractor(TransactionInformationExtractor):
	
	def getName(self):
		return "Belgium"

	def extractPossibleCompanyNames(self):
		return self.noticeText + self.getName()

	def extractCandidateCountries(self):
		return "Belgium"

	def extractRegistrationNumber(self):
		return "009"

	def getNoticeType(self):
		return "CBM"

	def extractCandidateRegNumbers(self,countries):
		return "CBM"

# ------------------------------------------------------------------------------------------- #
# ------------------------------------- END: DutchNoticeInformationExtractor -------------- #
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# ------------------------------------- Class to handle Dutch notices --------------------- #
# ------------------------------------------------------------------------------------------- #

class NetherlandsNoticeInformationExtractor(TransactionInformationExtractor):
	
	def getName(self):
		return "Netherlands"

	def extractPossibleCompanyNames(self):
		return self.noticeText + self.getName()

	def extractCandidateCountries(self):
		return "Netherlands"

	def extractRegistrationNumber(self):
		return "0010"

	def getNoticeType(self):
		return "CBM"

	def extractCandidateRegNumbers(self,countries):
		return "CBM"

# ------------------------------------------------------------------------------------------- #
# ------------------------------------- END: DutchNoticeInformationExtractor -------------- #
# ------------------------------------------------------------------------------------------- #