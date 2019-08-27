for %%i in (notices/*.pdf) do python TransactionInformationExtractorClient.py notices/%%i
python merge_csvs.py