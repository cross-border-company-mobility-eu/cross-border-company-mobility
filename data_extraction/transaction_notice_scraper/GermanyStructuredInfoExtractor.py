
# Function to remove empty string items from a list of strings
def removeBlanks(parts):
	result = []
	for part in parts:
		if part != '':
			result.append(part)
	return result

# Function to extract German company name from heading text of a notice
def extractGermanCompanyName(text):
	initialText = text + ""
	initialText = initialText[37:]
	initialText = initialText.lstrip()
	initialText = initialText[10:]
	parts = initialText.split('\n\n')
	if (len(parts) > 0):
		for item in parts:
			if ('' != item) and (' ' != item):
				return item.replace('\n','')
	else:
		return initialText.replace('\n','')
	
# Function to extract German company registration number
def extractGermanCompanyRegistrationNumber(text):
	initialText = text + ""
	initialText = initialText[20:]
	parts = initialText.split("(")
	if (len(parts) == 2):
		txt = parts[1].replace(")","")
		return txt.replace('\n','')
	else:
		return initialText.replace('\n','')

# Function to extract German company registration number
def extractTransactionDate(text):
	initialText = text + ""
	initialText = initialText[17:]
	initialText = initialText.lstrip()#
	initialText = initialText[:10]
	return initialText.replace('\n','')

# Function to remove German special characters from file
def getReadableEntity(text):
    return text