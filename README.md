![](html/assets/img/CbCM.png)


# Extracting information about a company transaction from a notice file

Instructions for running the script to extract information from the transaction notice PDF files.

Requirements:

+ [Python 3.7+](https://www.python.org/downloads/)
+ [pip 19+](https://pip.pypa.io/en/stable/installing/)
+ [Ruby 2.6.5+](https://www.ruby-lang.org/en/documentation/installation/)
+ [Git](http://git-scm.com/)

Steps:

#### Convert your PDF file(s) containing the relevant company transactions into text files:

1. After installing Ruby, run the following command from the command line or terminal: `gem install pdf-reader`. This will install a Ruby library to read PDF files.
2. Clone the following Github repository to your local machine: [https://github.com/horninc/parse-pdf-to-text-using-ruby](https://github.com/horninc/parse-pdf-to-text-using-ruby).
3. Open the terminal or command line. Navigate to the repository folder on your local machine which contains the script `parse.rb`.
4. Run the following commands from the terminal or command line: `mkdir pdfs` and `mkdir txts`.
5. Copy all the PDF file(s) that you want to convert into the `/pdfs` folder in this directory.
6. Run the following command from the terminal or command prompt: `ruby parse.rb`.
7. The converted versions of the PDF file(s) will be located in the `/txts` folder. 

#### Extract the relevant information from the notice file:

1. Clone this Github repository to your local machine using the command: `git clone https://github.com/maastrichtlawtech/cross-border-company-mobility.git`.
2. Navigate to the `/data_extraction/transaction_notice_scraper/` folder from your terminal or command line.
3. Install the required libraries for the extraction scripts by running: `pip install -r requirements.txt`. This may take a few minutes.
4. **For Mac/Linux users:** run the script `/data_extraction/transaction_notice_scraper/install_lang_models_linux_osx.sh` to install the required language modules. This may also take some time.
5. **For Windows users:** run the script `/data_extraction/transaction_notice_scraper/install_lang_models_win.bat` to install the required language modules. This may also take some time.
6. Copy the `.txt` versions of the transaction notice files from the `/txts` folder of the [https://github.com/horninc/parse-pdf-to-text-using-ruby](https://github.com/horninc/parse-pdf-to-text-using-ruby) repository, to the `/data_extraction/transaction_notice_scraper/` folder of this repository.
7. Run the following command from your terminal or command line: `python TransactionInformationExtractorClient.py [name-of-input-file].txt` where `[name-of-input-file]` is the name of the text version of the transaction notice file that you want to process. 
8. The output of the script will be a generated `.csv` file with the same name as the input text file that contains the relevant information about the transactions.