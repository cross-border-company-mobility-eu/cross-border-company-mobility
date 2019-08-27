# This script extracts all text from the German CBM PDF file and writes this output to text files.
# INPUT: German language PDF with list of notices for a year (e.g. 2019)
# OUTPUT:
# 1. .txt file with the raw text from the PDF file, including unrendered special characters
# 2. _readable.txt file with slash characters replaced by non-special characters
# USAGE: python pdftextextractor.py name_of_pdf_file.pdf
# example: python pdftextextractor.py germanyraw2019.pdf
# example output filename: "germanyraw2019.txt" and "germanyraw2019_readable.txt"

# import textract (PDF text extractor)
# import re (regular expression checker)
# import sys so we can parse commandline arguments
import textract
import re
import sys

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
    return text

# Preprocess PDF file argument

# Must have exactly two arguments (python file and PDF file)
if (len(sys.argv) != 2):
	raise Exception('Incorrect number of arguments. Exactly one argument with path to pdf file is required.')
	sys.exit()

# lower case the input file name
file_argument = sys.argv[1].lower()

# Must have PDF extension
if (file_argument[len(file_argument)-4:] != '.pdf'):
	raise Exception('this is not a valid pdf file')
	sys.exit()

# Extract entire PDF into one text variable
text = textract.process(sys.argv[1])
txt = str(text)

# Write the entire raw text extracted from the PDF to a text file
f = open(sys.argv[1][:len(file_argument)-4] + ".txt", "w")
f.write(txt)

# Write a more readable version of the file (with no special character encodings and slashes)
readableText = getReadableEntity(txt)
f = open(sys.argv[1][:len(file_argument)-4] + "_readable.txt", "w")
f.write(readableText)