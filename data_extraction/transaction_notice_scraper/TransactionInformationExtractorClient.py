# User / Client script
import re 													# Regular expression checker for Python
import sys 													# System libraries
import os 													# Operating System functions
import csv 													# CSV I/O library
from CountryNoticeInformationExtractors import * 			# Classes to handle the different countries notices 
from GermanyStructuredInfoExtractor import * 				# Helper functions to process text in german notice to extract structured info
from utility import getReadableEntity 						# Helper function to remove special characters from text

# Function to check if PDF is a document from Germany or Luxembourg Registry
def checkCountry(txt):
	fullNoticeStartIndexes = [m.start() for m in re.finditer('Handelsregister-Bekanntmachungen vom ', txt)]					# This piece of text is an indicator of a german notice file
	if (len(fullNoticeStartIndexes) >= 1):																					# If there is at least one notice
		return 'DE'																											# Germany
	elif "Recueil Electronique des Soci" in txt:																			# This piece of text at the start of the file is an indicator of a luxembourg notice
		return 'LU'																											# Luxembourg
	else:
		return '-'																											# Couldn't identify country

# Check number of command line arguments
if (len(sys.argv) != 2):
	raise Exception('Incorrect number of arguments. Exactly one argument with path to a .txt file is required.')
	sys.exit()

# lower case the input file name
file_argument = sys.argv[1].lower()

# Check for valid file extension
if (file_argument[len(file_argument)-4:] != '.txt'):
    raise Exception('this is not a valid .txt file')
    sys.exit()

# Extract entire PDF into one text variable
with open(file_argument, 'r') as file:
	data = file.read()
    #data = file.read().replace('\n', '')

    #text = textract.process(file_argument)
txt = data
#print(txt)

# Check which country this notice comes from
country = checkCountry(txt)

# Placeholder for output data
data = []

print("-------------------------------------")
print("Processing file...")

if country == 'DE':																											# If the input file is a Germany registry notice
	print("Germany registry file.")
	print("Indexing document...")
	# Get starting and ending indexes of important parts of the PDF text:
	# -------------------------------------------------------------------
	fullNoticeStartIndexes = [m.start() for m in re.finditer('Handelsregister-Bekanntmachungen vom ', txt)]					# Start points for each FULL notice in the PDF
	germanCompanyNameEndIndexes = [m.start() for m in re.finditer('Handelsregister-Nr.:', txt)]								# End points for the portion of the notice which contains the German company name
	noticeTextStartIndexes = [m.start() for m in re.finditer('Bekanntmachungstext', txt)]									# Start points for the notice TEXTS in the PDF
	noticeTextEndIndexes = [m.start() for m in re.finditer('Quelle:', txt)]													# End points for the notice TEXTS in the PDF
	regNumberTextStartIndexes = [m.start() for m in re.finditer('Handelsregister-Nr.:', txt)]								# Start points for the text containing registration numbers of the German companies
	regNumberTextEndIndexes = [m.start() for m in re.finditer('Amtsgericht:', txt)]											# End points for the text containing registration numbers of the German companies
	dateTextStartIndexes = [m.start() for m in re.finditer('Eintragungsdatum:', txt)]										# Start points for the text containing transaction dates
	dateTextEndIndexes = [m.start() for m in re.finditer('Bekanntmachungstext', txt)]										# End points for the text containing transaction dates
	# --------------------------------------------------------------------
	print("Indexing complete.")
	print("Preparing to iterate through notices...")
	print("----------------------------------------")
	#for i in range(1, 2):
	for i in range(0, 5):#len(fullNoticeStartIndexes)):
		#if (i+1 != 2):
		print("Processing notice " + str(i+1) + " of " + str(len(fullNoticeStartIndexes)))
		currentRow = []																										# Output data placeholder for current notice info
		# Get structured data from German notice
		noticeText = txt[noticeTextStartIndexes[i]:noticeTextEndIndexes[i]]													# Get the current notice text
		noticeText = noticeText[19:] 																						# Remove the heading part "Handelsregister-Nr."
		textContainingGermanCompanyName = txt[fullNoticeStartIndexes[i]:germanCompanyNameEndIndexes[i]]						# Get text containing the German company name for the current notice
		textContainingGermanCompanyRegistrationNumber = txt[regNumberTextStartIndexes[i]:regNumberTextEndIndexes[i]]		# Get text containing the German company registration number for the current notice
		textContainingTransactionDate = txt[dateTextStartIndexes[i]:dateTextEndIndexes[i]]									# Get text containing the transaction date for the current notice
		germanCompanyName = extractGermanCompanyName(textContainingGermanCompanyName)										# Remove irrelevant information from the text to reveal the German company name
		germanCompanyRegNumber = extractGermanCompanyRegistrationNumber(textContainingGermanCompanyRegistrationNumber)		# Remove irrelevant information from the text to reveal the German company registraton number
		transactionDate = extractTransactionDate(textContainingTransactionDate)												# Remove irrelevant information from the text to reveal the transaction date of the current notice
		# Append structured data to row
		currentRow.append(transactionDate)																					# Add transaction date to output data												
		currentRow.append(germanCompanyName)																				# Add German company name to output data
		currentRow.append('DE')  																							# Add Germany code to output data
		currentRow.append(germanCompanyRegNumber)																			# Add Germany company registration number to output data
		# Get unstructured data from German notice
		g = GermanyNoticeInformationExtractor(noticeText)																	# Initialise Germany notice information extractor
		candidateCompanies = g.extractPossibleCompanyNames()																# Possible non-german companies
		companyName = g.extractNonGermanCompany(germanCompanyName)															# Try to extract one 
		#if (len(companyName) == 0):																							# If couldn't find one
		companyName.extend(candidateCompanies)																			# add the other possibilities found earlier
		country = g.extractNonGermanCompanyCountry()																		# Non-german country
		noticeType = g.getNoticeType()																						# CBM/ST/SE?
		# Append unstructured data to row
		currentRow.append(companyName)																						# Companies
		currentRow.append(country)																							# Country
		if (country == "-"):																								# If I don't know the country of the company
			regNumbers = g.extractCandidateRegNumbers(g.extractCandidateCountries())										# Try to extract all possible registration numbers
			currentRow.append(regNumbers)																					# Add all possible registration numbers to the output
		else:
			regNumber = g.extractRegistrationNumber(country)																# Otherwise, just get the registration number that conforms to the country format
			currentRow.append(regNumber)																					# Add single registration number to output
		currentRow.append(noticeType)																						# Append transaction type CBM/ST/SE to output data
		currentRow.append(getReadableEntity(noticeText))																	# Original notice text (german)
		currentRow.append(getReadableEntity(g.getEnglishNotice()))															# English translation of notice
		data.append(currentRow)															
	print("-------------------------------------------------")
	file_argument2 = file_argument.replace(file_argument[len(file_argument)-4:],"")											# Get filename of the input notice file (without extension). We will use the same filename for the output CSV file
	print("Writing information to " + str(file_argument2) + ".csv...")					
	header = ["date","german_company","country1","registration_number1",													# Create header (column labels) for CSV output file
	"other_company","country2","registration_number2","transaction_type",													# Create header (column labels) for CSV output file
	"notice_text","english_notice_text"]																					# Create header (column labels) for CSV output file																						
	data.insert(0,header)																									# Insert header of CSV file at the beginning of the output list
	with open(str(file_argument2) + ".csv", "w", newline="", encoding="utf-8") as f:															# Open CSV file for output
	    writer = csv.writer(f)																								# Initialise a CSV writer object
	    writer.writerows(data)																								# Write output to file
	print("Successfully wrote information to file.")
	print()
elif country == 'LU':																										# If the input file is a luxembourg registry notice
	print("Luxembourg registry file.")
	print("Indexing document...")
	print("Indexing complete.")
	print("Processing notice...")
	print()
	utext = re.sub(r'[^\x00-\x7f]',r'', txt)																				# Remove unicode characters
	l = LuxembourgNoticeInformationExtractor(utext)																			# Initialise Luxembourg notice information extractor
	companies = l.extractPossibleCompanyNames()																				# Extract possible company names from notice
	noticeType = l.getNoticeType()																							# CBM/ST/SE?
	print("Notice type: " + noticeType)
	print()
	print("Companies: ")
	print(companies)
	print()
	print("-------------------------------------------------")
else:
	print("Unknown registry file.")

print("DONE.")
print("-------------------------------------------------")