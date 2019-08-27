import csv                              # I/O of CSV files
from google.cloud import translate      # Import translate module from Google Cloud services
import os                               # Operating system specific methods 
import re								# Regular expressions library
from textblob import TextBlob
import string

# Set Google API key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\kody.moodley\\Documents\\Coding\\cbcm-be7e7645e0ec.json"

#translator = Translator()                          # initialize translator service
translate_client = translate.Client()               # Create Google Cloud Translate API service 

# Function to remove unrendered unicode characters from a raw string
# Parameter:    the text to remove characters from
# Output:       the text minus the special characters  
# Notes:        depending on the OS (windows, mac, linux), the number of slashes may change
def getReadableEntity(text):
	text = text.replace("\\r\\n", " ")
	text = text.replace("\\xc3\\xbc", "u")
	text = text.replace("\\xc3\\xa4", "a")
	text = text.replace("\\xc2\\xa7", "")
	text = text.replace("\\xc3\\x9f", "ss")
	text = text.replace("\\xc3\\xb6", "o")
	text = text.replace("\\xc3\\x84", "A")
	text = text.replace("\\xc3\\x9c", "U")
	text = text.replace("\\xc3\\xa9", "e")
	text = text.replace("\\xc3\\xa8", "e")
	text = text.replace("\\xc3\\x96", "O")
	text = text.replace("\\xc3\\xa0 r", "\\xc3\\xa0.r")
	text = text.replace("\\xc3\\xa0", "a")
	text = text.replace("\r\n", " ")
	text = text.replace("\xc3\xbc", "u")
	text = text.replace("\xc3\xa4", "a")
	text = text.replace("\xc2\xa7", "")
	text = text.replace("\xc3\x9f", "ss")
	text = text.replace("\xc3\xb6", "o")
	text = text.replace("\xc3\x84", "A")
	text = text.replace("\xc3\x9c", "U")
	text = text.replace("\xc3\xa9", "e")
	text = text.replace("\xc3\xa8", "e")
	text = text.replace("\xc3\x96", "O")
	text = text.replace("\xc3\xa0 r", "\xc3\xa0.r")
	text = text.replace("\xc3\xa0", "a")
	text = text.replace("'", "'")
	return text

# Identify notices that contain unknown companies
# Parameter 1: a list of company names
# Parameter 2: a list of notices (text)
# Output:      the subset of the list of input notices that do not contain any of the input company names
def getUnknownCompanies(knowncompanies, notices):
	result = []
	for notice in notices:
		found = False
		for company in knowncompanies:
			if (is_kw_in_notice(company, notice)):
				found = True
		if found:
			pass
		else:
			result.append(notice)
	return result

# Function to compute the intersection of multiple sets
# Parameters:   list of sets e.g. intersect(set1, set2, set3)
# Output:       a set of items that appear in each of the input sets
def intersect(*d):
	sets = []
	for i in range(1, len(d)):
		sets.append(d[i])
	result = set(d[0])
	for s in sets:
		result = result.intersection(set(s))
	return result

# Function to perform set difference computation (e.g. setA - setB)
# Parameter 1:  a set - set A
# Parameter 2:  another set - set B
# Output:       the set of things in Set A that do not appear in Set B
def setDifference(setA, setB):
	result = []
	for item in setA:
		if (item not in setB):
			result.append(item)
	return result

# Function to check if a given keyword appears in a piece of text
# Parameter 1:  keyword to identify in the text
# Parameter 2:  the text in which to search for the given keyword
# Output:       the index of the start of the given keyword in the text (e.g. "3") or "-1" in the case that the keyword does not appear in the text
def is_kw_in_notice(kw, text):
	return  text.lower().find(kw)

# Function to find the subset of notices in a list that contain a given keyword
# Parameter 1:  list of notices
# Parameter 2:  keyword to identify in the notices
# Output:       the list of notices which actually contain the keyword in them
def find_relevant_notices_kw(notices, kw):
	result = []
	for notice in notices:
		if (notice.lower().find(kw) != -1):
			result.append(notice)
	return result

# Function to determine if a SINGLE notice contains a given keyword
# Parameter 1:  a single notice text
# Parameter 2:  keyword to identify in the notice
# Output:       "True" if the keyword appears in the notice, "False" otherwise
def is_relevant_notice_kw(notice, kw):
	if (notice.lower().find(kw) != -1):
		return True
	return False

# Function to do AND and OR search for multiple keywords in a notice
# Parameter 1:  a single notice text
# Parameter 2:  either a single keyword to identify in the notice OR a list of keywords to search for
# Parameter 3:  a switch to determine if the search is to be interpreted as an AND or an OR keyword search. Expects 'and' for AND search, if any other string is given it will be interpreted as OR search
# Output:       If a single keyword is given, returns "True" if the keyword appears in the notice. 
# Output:       If a LIST of keywords is given, and queryType = 'and', returns "True" if ALL keywords in the list appear in the notice, returns "False" otherwise
# Output:       If a LIST of keywords is given, and queryType != 'and', returns "True" if AT LEAST ONE keyword appears in the notice, returns "False" otherwise
def is_relevant_notice(notice, kw, queryType):
	if (isinstance(kw, str)):
		return is_relevant_notice_kw(notice, kw)

	if (queryType == 'and'):                            # AND (contains all keywords)
		noticeIsRelevant = True
		idx = 0
		while noticeIsRelevant and idx < len(kw):
			noticeIsRelevant = is_relevant_notice_kw(notice, kw[idx])
			idx += 1
		if noticeIsRelevant:
			return True
		else:
			return False
	else:                                               # OR (contains at least one keyword) 
		noticeIsRelevant = False
		idx = 0
		while (not noticeIsRelevant) and (idx < len(kw)):
			noticeIsRelevant = is_relevant_notice_kw(notice, kw[idx])
			idx += 1
		if noticeIsRelevant:
			return True
		else:
			return False

# Function to find relevant notices in the list based on a keyword search query
# Parameter 1:  a LIST of notices
# Parameter 2:  either a single keyword to identify in the notice OR a list of keywords to search for
# Parameter 3:  a switch to determine if the search is to be interpreted as an AND or an OR keyword search. Expects 'and' for AND search, if any other string is given it will be interpreted as OR search
# Output:       If a single keyword is given, returns the subset of given notices that contain the given keyword
# Output:       If a LIST of keywords is given, and queryType = 'and', returns the subset of given notices that contain ALL of the given keywords
# Output:       If a LIST of keywords is given, and queryType != 'and', returns the subset of given notices that contain AT LEAST ONE of the given keywords
def find_relevant_notices(notices, kw, queryType):
	if (isinstance(kw, str)):
		return find_relevant_notices_kw(notices, kw)

	if (queryType == 'and'):                            # AND (contains all keywords)
		result = []
		for k in kw:
			tmp = find_relevant_notices_kw(notices, k)
			result.append(tmp)
		return intersect(*result)
	else:                                               # OR (contains at least one keyword) 
		result = []
		for k in kw:
			tmp = find_relevant_notices_kw(notices, k)
			result.extend(tmp)
		return list(set(result))

# Function to eliminate strings in a list that have longer strings that include them (in the same list)
# Example:      input -> ['af', 'ab' , 'abc', 'baf'], output -> ['abc', 'baf']
# Parameter:    a list of strings
# Output:       the subset of strings from the input list that satisfies the condition described in "Example" above
def find_supersets(strings):
	superstrings = set()
	set_to_string = dict(zip([frozenset(s.split()) for s in strings], strings))
	for s in set_to_string.keys():
		for sup in superstrings.copy():
			if s <= sup:
				break
			elif sup < s:
				superstrings.remove(sup)
		else:
			superstrings.add(s)
	return [set_to_string[sup] for sup in superstrings]

# ?
def using_sorted(strings):
	stsets = sorted(
		(frozenset(s.split()) for s in strings), key=len, reverse=True)
	superstrings = set()
	for stset in stsets:
		if not any(stset.issubset(s) for s in superstrings):
			superstrings.add(stset)
	return superstrings

# Function to import an entire CSV file into a 2-d array
# Paramter:    filename of CSV file to import
# Output:      2-d array containing all rows of the CSV file
def importcsvfile(filename):
	rows = []
	with open(filename, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			rows.append(row)
	return rows

# Function to import a single column from a CSV file into a 1-d array
# Paramter 1:   filename of CSV file to import
# Paramter 2:   the index of the column to import
# Output:       1-d array representing the information in the specified column from the CSV file
def importcolumnfromcsvfile(filename,columnnumber):
	rows = []
	with open(filename, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			rows.append(row[3])
	return rows

# Function that removes duplicate companies from a list of companies and removes special characters from the names
# Parameter:    a list of company names
# Output:       a subset of the input list that are unique (with special characters removed)
def cleanCompanies(companies):
	tmpCompanies = []
	tmpCompanies.extend(companies)
	tmpCompanies = list(set(tmpCompanies))
	result = []
	for company in tmpCompanies:
		result.append(getReadableEntity(company))
	return result

# Function to detect the language of a piece of text
# Parameter: "text" - the text to detect the language of
# Output: returns a two-digit language code representing the language of the text e.g. "fr" for french
def detectlang(text):
	langdetect = TextBlob(text)
	return langdetect.detect_language()

# Function to translate the notice text to english (USING GOOGLE CLOUD TRANSLATE API)
# Parameter:    input text to translate to English
# Output:       the translated text in English   
def translateToEnglish(text):
	result = translate_client.translate(getReadableEntity(text), target_language='en')
	return u'{}'.format(result['translatedText'])

# Function to check if candidate company name actually has a valid legal form
# Parameter:    string representing or containing a company name (if contains multiple company names it will return first match found)
# Output:       returns the company form of the given company if it contains one, otherwise returns "False"     
def containsCompanyForm(text):
	s=text
	if re.search(r" (b|B)(\.| |\. |)(v|V)(\.|)", s): #BV
		return 'BV'
	elif re.search(r"G(\.|es\.|\. | |)(m|M)(\.|\. | |)(b|B)(\.|\. | |)(h|H)(\.|)", s): #GMBH
		return 'GMBH'
	elif re.search(r"(s|S)(\.| |)(a|à)(\.| |)r(\.| |)l(\.|)", s): #SARL
		return 'SARL'
	elif re.search(r"(s|S)(\.|)(p|P)(\.|)(r|R)(\.|)(l|L)(\.|)", s): #SPRL
		return 'SPRL'
	elif re.search(r"(b|B)(\.| |)(v|V)(\.| |)(b|B)(\.| |)(a|A)(\.|)", s): #BVBA
		return 'BVBA'
	elif re.search(r"Ltd.|Limited|LIMITED", s): # LTD
		return 'LTD'
	elif re.search(r"d(\.|\. | |)o(\.|\. | |)o(\.|)", s): # doo
		return 'doo'
	elif re.search(r"s\.r\.o\.", s): # sro
		return 'sro'
	elif re.search(r"OOD", s): # OOD
		return 'OOD'
	elif re.search(r"ООД", s): # OOX
		return 'OOX'
	elif re.search(r"ApS", s): # ApS
		return 'ApS'
	elif re.search(r"OÜ", s): # OU
		return 'OU'
	elif re.search(r"OY", s): # OY
		return 'OY'
	elif re.search(r" AB", s): # AB
		return 'AB'
	elif re.search(r"E\.P\.E\.", s): # EPE
		return 'EPE'
	elif re.search(r"kft\.", s): # kft
		return 'kft.'
	elif re.search(r"S\.r\.l\.", s): # S.r.l.
		return 'S.r.l.'
	elif re.search(r"SIA", s): # SIA
		return 'SIA'
	elif re.search(r"UAB", s): # UAB
		return 'UAB'
	elif re.search(r"AS ", s): # AS
		return 'AS'
	elif re.search(r"(sp\. |)z\.o\.o\.", s): # z.o.o.
		return 'z.o.o.'
	elif re.search(r"Lda\.", s): # Lda.
		return 'Lda.'
	elif re.search(r"SRL", s): # SRL
		return 'SRL'
	elif re.search(r"ehf\.", s): # ehf.
		return 'ehf.'
	elif re.search(r" (a|A)(\.| |\. |)(g|G)(\.|)", s): # AG
		return 'AG'
	elif re.search(r" (n|N)(\.| |\. |)(v|V)(\.|)", s): # NV
		return 'NV'
	elif re.search(r" (s|S)(\.| |\. |)(a|A)(\.|)", s): # SA
		return 'SA'
	elif re.search(r"AD", s): # AD
		return 'AD'
	elif re.search(r"AД ", s): # AД
		return 'AX'
	elif re.search(r"d\.d\.", s): # d.d.
		return 'd.d.'
	elif re.search(r"PLC", s): # PLC
		return 'PLC'
	elif re.search(r"a\.s\.", s): # a.s.
		return 'a.s.'
	elif re.search(r"A\/S", s): # A/S
		return 'A/S'
	elif re.search(r"AS", s): # AS
		return 'AS'
	elif re.search(r"Oyj", s): # Oyj
		return 'Oyj'
	elif re.search(r"Abp ", s): # Abp
		return 'Abp'
	elif re.search(r"ASA ", s): # ASA
		return 'ASA'
	elif re.search(r"AB (publ)", s): # Oyj
		return 'AB'
	elif re.search(r"hf\.", s): # hf.
		return 'hf.'
	elif re.search(r"SE ", s): # SE
		return 'SE'
	elif re.search(r"SCE ", s): # SCE
		return 'SCE'
	elif re.search(r"SICAV", s): # SICAV
		return 'SICAV'
	elif re.search(r"SEM ", s): # SEM
		return 'SEM'
	elif re.search(r"s\.p\.", s): # s.p.
		return 's.p.'
	else:
		return False


# Function to check if candidate company name actually has a valid legal form
# Parameter:    string representing or containing a company name (if contains multiple company names it will return first match found)
# Output:       returns the company form of the given company if it contains one, otherwise returns "False"     
def getCompanyFormPositionsInText(text):
	s=text
	companyFormPositions = []

	bvs = re.finditer(r"(b|B)(\.| |\. |)(v|V)(\.|)", s) #BV
	for bv in bvs:
		currMatchPos = []
		currMatchPos.append("BV")
		currMatchPos.append(bv.start())
		currMatchPos.append(bv.end())
		companyFormPositions.append(currMatchPos)

	gmbhs = re.finditer(r"G(\.|es\.|\. | |)(m|M)(\.|\. | |)(b|B)(\.|\. | |)(h|H)(\.|)", s) #GMBH
	#print(gmbhs)
	for gmbh in gmbhs:
		currMatchPos = []
		currMatchPos.append("GmbH")
		currMatchPos.append(gmbh.start())
		currMatchPos.append(gmbh.end())
		companyFormPositions.append(currMatchPos)

	sarls = re.finditer(r"(s|S)(\.| |)(a|à)(\.| |)r(\.| |)l(\.|)", s) #SARL
	for sarl in sarls:
		currMatchPos = []
		currMatchPos.append("SARL")
		currMatchPos.append(sarl.start())
		currMatchPos.append(sarl.end())
		companyFormPositions.append(currMatchPos)

	sprls = re.finditer(r"(s|S)(\.|)(p|P)(\.|)(r|R)(\.|)(l|L)(\.|)", s) #SPRL
	for sprl in sprls:
		currMatchPos = []
		currMatchPos.append("SPRL")
		currMatchPos.append(sprl.start())
		currMatchPos.append(sprl.end())
		companyFormPositions.append(currMatchPos)
	
	bvbas = re.finditer(r"(b|B)(\.| |)(v|V)(\.| |)(b|B)(\.| |)(a|A)(\.|)", s) #BVBA
	for bvba in bvbas:
		currMatchPos = []
		currMatchPos.append("BVBA")
		currMatchPos.append(bvba.start())
		currMatchPos.append(bvba.end())
		companyFormPositions.append(currMatchPos)

	ltds = re.finditer(r"Ltd.|Limited|LIMITED|L.t.d.", s) #LTD
	for ltd in ltds:
		currMatchPos = []
		currMatchPos.append("Ltd")
		currMatchPos.append(ltd.start())
		currMatchPos.append(ltd.end())
		companyFormPositions.append(currMatchPos)

	doos = re.finditer(r"d(\.|\. | |)o(\.|\. | |)o(\.|)", s) #doo
	for doo in doos:
		currMatchPos = []
		currMatchPos.append("doo")
		currMatchPos.append(doo.start())
		currMatchPos.append(doo.end())
		companyFormPositions.append(currMatchPos)

	sros = re.finditer(r"s\.r\.o\.", s) #sro
	for sro in sros:
		currMatchPos = []
		currMatchPos.append("SRO")
		currMatchPos.append(sro.start())
		currMatchPos.append(sro.end())
		companyFormPositions.append(currMatchPos)

	oods = re.finditer(r"OOD", s) #ood
	for ood in oods:
		currMatchPos = []
		currMatchPos.append("OOD")
		currMatchPos.append(ood.start())
		currMatchPos.append(ood.end())
		companyFormPositions.append(currMatchPos)

	ooxs = re.finditer(r"ООД", s) #oox
	for oox in ooxs:
		currMatchPos = []
		currMatchPos.append("OOД")
		currMatchPos.append(oox.start())
		currMatchPos.append(oox.end())
		companyFormPositions.append(currMatchPos)

	apss = re.finditer(r"ApS", s) #ApS
	for aps in apss:
		currMatchPos = []
		currMatchPos.append("ApS")
		currMatchPos.append(aps.start())
		currMatchPos.append(aps.end())
		companyFormPositions.append(currMatchPos)

	ous = re.finditer(r"OÜ", s) #OU
	for ou in ous:
		currMatchPos = []
		currMatchPos.append("OÜ")
		currMatchPos.append(ou.start())
		currMatchPos.append(ou.end())
		companyFormPositions.append(currMatchPos)

	oys = re.finditer(r"OY", s) #OY
	for oy in oys:
		currMatchPos = []
		currMatchPos.append("OY")
		currMatchPos.append(oy.start())
		currMatchPos.append(oy.end())
		companyFormPositions.append(currMatchPos)

	abss = re.finditer(r"AB", s) #AB
	for ab in abss:
		currMatchPos = []
		currMatchPos.append("AB")
		currMatchPos.append(ab.start())
		currMatchPos.append(ab.end())
		companyFormPositions.append(currMatchPos)

	epes = re.finditer(r"E\.P\.E\.", s) #EPE
	for epe in epes:
		currMatchPos = []
		currMatchPos.append("EPE")
		currMatchPos.append(epe.start())
		currMatchPos.append(epe.end())
		companyFormPositions.append(currMatchPos)

	kfts = re.finditer(r"kft\.", s) #Kft
	for kft in kfts:
		currMatchPos = []
		currMatchPos.append("KFT")
		currMatchPos.append(kft.start())
		currMatchPos.append(kft.end())
		companyFormPositions.append(currMatchPos)

	srls = re.finditer(r"S\.r\.l\.|SRL|srl|Srl", s) #S.r.l
	for srl in srls:
		currMatchPos = []
		currMatchPos.append("SRL")
		currMatchPos.append(srl.start())
		currMatchPos.append(srl.end())
		companyFormPositions.append(currMatchPos)

	sias = re.finditer(r"SIA", s) #SIA
	for sia in sias:
		currMatchPos = []
		currMatchPos.append("SIA")
		currMatchPos.append(sia.start())
		currMatchPos.append(sia.end())
		companyFormPositions.append(currMatchPos)

	uabs = re.finditer(r"UAB", s) #UAB
	for uab in uabs:
		currMatchPos = []
		currMatchPos.append("UAB")
		currMatchPos.append(uab.start())
		currMatchPos.append(uab.end())
		companyFormPositions.append(currMatchPos)

	as_set = re.finditer(r"AS|a\.s\.|As", s) #AS
	for as_el in as_set:
		currMatchPos = []
		currMatchPos.append("AS")
		currMatchPos.append(as_el.start())
		currMatchPos.append(as_el.end())
		companyFormPositions.append(currMatchPos)

	as_set = re.finditer(r"AS ", s) #AS
	for as_el in as_set:
		currMatchPos = []
		currMatchPos.append("AS")
		currMatchPos.append(as_el.start())
		currMatchPos.append(as_el.end())
		companyFormPositions.append(currMatchPos)

	zoos = re.finditer(r"(sp\. |)z\.o\.o\.", s) #Z.o.o
	for zoo in zoos:
		currMatchPos = []
		currMatchPos.append("Z.O.O")
		currMatchPos.append(zoo.start())
		currMatchPos.append(zoo.end())
		companyFormPositions.append(currMatchPos)

	ldas = re.finditer(r"Lda\.", s) #Lda.
	for lda in ldas:
		currMatchPos = []
		currMatchPos.append("LDA")
		currMatchPos.append(lda.start())
		currMatchPos.append(lda.end())
		companyFormPositions.append(currMatchPos)

	ehfs = re.finditer(r"ehf\.", s) #ehf.
	for ehf in ehfs:
		currMatchPos = []
		currMatchPos.append("EHF")
		currMatchPos.append(ehf.start())
		currMatchPos.append(ehf.end())
		companyFormPositions.append(currMatchPos)

	ags = re.finditer(r" (a|A)(\.| |\. |)(g|G)(\.|)", s) #AG
	for ag in ags:
		currMatchPos = []
		currMatchPos.append("AG")
		currMatchPos.append(ag.start())
		currMatchPos.append(ag.end())
		companyFormPositions.append(currMatchPos)

	nvs = re.finditer(r" (n|N)(\.| |\. |)(v|V)(\.|)", s) #NV
	for nv in nvs:
		currMatchPos = []
		currMatchPos.append("NV")
		currMatchPos.append(nv.start())
		currMatchPos.append(nv.end())
		companyFormPositions.append(currMatchPos)

	sas = re.finditer(r" (s|S)(\.| |\. |)(a|A)(\.|)", s) #SA
	for sa in sas:
		currMatchPos = []
		currMatchPos.append("SA")
		currMatchPos.append(sa.start())
		currMatchPos.append(sa.end())
		companyFormPositions.append(currMatchPos)

	ads = re.finditer(r"AD", s) #AD
	for ad in ads:
		currMatchPos = []
		currMatchPos.append("AD")
		currMatchPos.append(ad.start())
		currMatchPos.append(ad.end())
		companyFormPositions.append(currMatchPos)

	axs = re.finditer(r"AД ", s) #AД
	for ax in axs:
		currMatchPos = []
		currMatchPos.append("AД")
		currMatchPos.append(ax.start())
		currMatchPos.append(ax.end())
		companyFormPositions.append(currMatchPos)

	dds = re.finditer(r"d\.d\.", s) #DD
	for dd in dds:
		currMatchPos = []
		currMatchPos.append("DD")
		currMatchPos.append(dd.start())
		currMatchPos.append(dd.end())
		companyFormPositions.append(currMatchPos)

	plcs = re.finditer(r"PLC", s) #PLC
	for plc in plcs:
		currMatchPos = []
		currMatchPos.append("PLC")
		currMatchPos.append(plc.start())
		currMatchPos.append(plc.end())
		companyFormPositions.append(currMatchPos)

	aslashss = re.finditer(r"A\/S", s) #A/S
	for aslashs in aslashss:
		currMatchPos = []
		currMatchPos.append("A/S")
		currMatchPos.append(aslashs.start())
		currMatchPos.append(aslashs.end())
		companyFormPositions.append(currMatchPos)

	oyjs = re.finditer(r"Oyj", s) #Oyj
	for oyj in oyjs:
		currMatchPos = []
		currMatchPos.append("OYJ")
		currMatchPos.append(oyj.start())
		currMatchPos.append(oyj.end())
		companyFormPositions.append(currMatchPos)

	abps = re.finditer(r"Abp ", s) #Abp
	for abp in abps:
		currMatchPos = []
		currMatchPos.append("Abp")
		currMatchPos.append(abp.start())
		currMatchPos.append(abp.end())
		companyFormPositions.append(currMatchPos)

	asas = re.finditer(r"ASA ", s) #ASA
	for asa in asas:
		currMatchPos = []
		currMatchPos.append("ASA")
		currMatchPos.append(asa.start())
		currMatchPos.append(asa.end())
		companyFormPositions.append(currMatchPos)

	asas = re.finditer(r"ASA ", s) #ASA
	for asa in asas:
		currMatchPos = []
		currMatchPos.append("ASA")
		currMatchPos.append(asa.start())
		currMatchPos.append(asa.end())
		companyFormPositions.append(currMatchPos)

	abpubs = re.finditer(r"AB (publ)", s) #AB publ
	for abpub in abpubs:
		currMatchPos = []
		currMatchPos.append("AB (publ)")
		currMatchPos.append(abpub.start())
		currMatchPos.append(abpub.end())
		companyFormPositions.append(currMatchPos)

	hfs = re.finditer(r"hf\.", s) #Hf.
	for hf in hfs:
		currMatchPos = []
		currMatchPos.append("HF")
		currMatchPos.append(hf.start())
		currMatchPos.append(hf.end())
		companyFormPositions.append(currMatchPos)

	ses = re.finditer(r"SE ", s) #SE
	for se in ses:
		currMatchPos = []
		currMatchPos.append("SE")
		currMatchPos.append(se.start())
		currMatchPos.append(se.end())
		companyFormPositions.append(currMatchPos)

	sces = re.finditer(r"SCE", s) #SCE
	for sce in sces:
		currMatchPos = []
		currMatchPos.append("SCE")
		currMatchPos.append(sce.start())
		currMatchPos.append(sce.end())
		companyFormPositions.append(currMatchPos)

	sicavs = re.finditer(r"SICAV", s) #SICAV
	for sicav in sicavs:
		currMatchPos = []
		currMatchPos.append("SICAV")
		currMatchPos.append(sicav.start())
		currMatchPos.append(sicav.end())
		companyFormPositions.append(currMatchPos)

	sems = re.finditer(r"SEM", s) #SEM
	for sem in sems:
		currMatchPos = []
		currMatchPos.append("SEM")
		currMatchPos.append(sem.start())
		currMatchPos.append(sem.end())
		companyFormPositions.append(currMatchPos)

	sps = re.finditer(r"s\.p\.", s) #S.P.
	for sp in sps:
		currMatchPos = []
		currMatchPos.append("SP")
		currMatchPos.append(sp.start())
		currMatchPos.append(sp.end())
		companyFormPositions.append(currMatchPos)

	return companyFormPositions

# Removes whitespace from left and right of string
# Removes punctuation from string
# Lowercases string
def cleanCompanyName(companyName):
	tmp = companyName
	tmp = tmp.lstrip()
	tmp = tmp.rstrip()
	tmp = tmp.translate(str.maketrans('','',string.punctuation))
	return tmp.lower()

# Function to modify some parts of the notice text (I found that this affects the accuracy of Spacy's entity recognition algorithms)
# Parameter:    original notice text
# Output:       the processed text
def preprocessNoticeText(text):
	text = text.replace("LIMITED","Ltd")
	text = text.replace("Limited","Ltd")
	text = text.replace("GmbH"," GmbH")
	text = text.replace("gmbh"," GmbH")
	text = text.replace("software"," software")
	text = text.replace("TECHNOLOGY","Technology")
	text = text.replace("HOLDING","Holding")
	#   S. a r. l.
	text = text.replace(" s.a.r.l "," Sarl ")
	text = text.replace("s.a.r.l ","Sarl ")
	text = text.replace("s.a.r.l","Sarl")
	text = text.replace("S.a.r.l","Sarl")
	text = text.replace("S. a r. l","Sarl")
	text = text.replace("S. a r.l","Sarl")
	text = text.replace("S.a r.l","Sarl")
	text = text.replace("Sa.r.l","Sarl")
	text = text.replace(" sar "," Sarl ")
	text = text.replace(" SAR "," Sarl ")
	text = text.replace(" Sar "," Sarl ")
	text = text.replace(" s a r l "," Sarl ")
	text = text.replace(" S A R L "," Sarl ")
	text = text.replace(" S a r l "," Sarl ")
	text = text.replace(" sarl "," Sarl ")
	# company
	# text = text.replace("the company","entity")
	# text = text.replace("the Company","entity")
	# text = text.replace("The company","entity")
	# text = text.replace("The Company","entity")
	# text = text.replace("Transferring Company","entity")
	# text = text.replace("Transferring company","entity")
	# text = text.replace("transferring Company","entity")
	# text = text.replace("transferring company","entity")
	# text = text.replace("Merging Company","entity")
	# text = text.replace("Merging company","entity")
	# text = text.replace("merging Company","entity")
	# text = text.replace("merging company","entity")
	# other
	#text = text.replace(":","")
	#text = text.replace("&","")
	return text
