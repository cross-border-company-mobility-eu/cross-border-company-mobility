# Function to remove empty string items from a list of strings
def removeBlanks(parts):
	result = []
	for part in parts:
		if part != '':
			result.append(part)
	return result

# Function to extract German company name from heading text of a notice
def extractGermanCompanyName(text):
	#print(text)
	initialText = text + ""
	initialText = initialText[37:]
	#print(initialText)
	stringparts = initialText.split("\\r\\n\\r\\n")
	#print(stringparts)
	#print(stringparts[1])
	companyNameParts = stringparts[1].split("\\r\\n")
	#print(companyNameParts)
	#print(companyNameParts[0])
	return companyNameParts[0]

# Function to extract German company registration number
def extractGermanCompanyRegistrationNumber(text):
	initialText = text + ""
	initialText = initialText[20:]
	initialText = initialText.replace("\\r\\n", "")
	return initialText

# Function to extract German company registration number
def extractTransactionDate(text):
	initialText = text + ""
	initialText = initialText[17:]
	dateParts = initialText.split("\\r\\n")
	dateParts = removeBlanks(dateParts)
	return dateParts[0]

# Function to remove German special characters from file
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
    text = text.replace("\xc3\xa0", "a")
    return text