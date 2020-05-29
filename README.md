# CryptoNews

CryptoNews is a API based on Flask that displays the latest news about cryptocurrencies.

ETL ETL ETL

## Components:
1) `extract.py`: fetching the latest news from newsapi.org for the keywords: crypto, bitcoin and ethereum
Automated task: every 5 minutes
2) `transform.py`: data parsing 
3) `load.py`: load parsed data into MySQL server
