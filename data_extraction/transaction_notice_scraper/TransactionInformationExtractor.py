import nltk																	# NLP toolkit for Python - https://www.nltk.org/
import spacy    															# Another NLP toolkit for Python - https://spacy.io/
from abc import ABC, abstractmethod											# Enable usage of Python abstract classes and methods							
from utility import translateToEnglish,detectlang,getReadableEntity			# Import helper functions from utility class

class TransactionInformationExtractor(ABC):
	# load language models for spacy NLP toolkit
	germannlp 	= spacy.load('de_core_news_sm') 							# german language model for spacy
	englishnlp 	= spacy.load('en_core_web_sm')      						# english language model for spacy
	frenchnlp 	= spacy.load("fr_core_news_sm")								# french language model for spacy
	dutchnlp 	= spacy.load("nl_core_news_sm")								# dutch language model for spacy
	# Constructor accepts notice text
	def __init__(self, noticeText):
		self.language = detectlang(noticeText)
		self.noticeText = getReadableEntity(noticeText)
		print("Notice language: " + self.language)
		if (self.language != 'en'):
			self.englishNoticeText 	= translateToEnglish(self.noticeText)	# Store an English version of the notice
		else:
			self.englishNoticeText = self.noticeText
		
		super().__init__()

	@abstractmethod
	# Description: 	Obtain a list of entities that could possibly be company names in the piece of text (the candidates)
	# Output: 		a list of phrases or words in the text that could be company names (organisations, persons, geopolitical locations and miscellaneous entities)
	def extractPossibleCompanyNames(self):
		pass
   
	@abstractmethod
	# Description:	Function to extract countries mentioned in a notice
	# Output: 		a list of countries appearing in the notice
	def extractCandidateCountries(self):
		pass

	@abstractmethod
	# Description: 	Function to extract the registration number of the company involved in the transaction which is NOT from the notice registry country
	# Parameter: 	country from which the company comes from
	# Output: 		registration number of the company
	def extractRegistrationNumber(self, country):
		pass

	@abstractmethod
	# Description: 	Function to extract the registration number of the company involved in the transaction which is NOT from the notice registry country
	# Parameter: 	list of countries mentioned in the notice
	# Output: 		Registration numbers of companies mentioned in the notice
	def extractCandidateRegNumbers(self,countries):
		pass
  
	@abstractmethod
	# Description:	Function to classify the notice as either a CBM, ST or SE
	# Output: 		'CBM', 'ST', 'SE' or '??' if unknown
	def getNoticeType(self):
		pass