#!/usr/bin/python3.7

import requests
import datetime
import json
#import sys
#sys.path.append('../')
from CN_config import apiKey

def get_top_headlines(country, apiKey=apiKey):
    URL = ('http://newsapi.org/v2/top-headlines?'
        f'country={country}&'
        f'apiKey={apiKey}')
    data = requests.get(URL).json()
    timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M")
    with open(f'data/TOP-H_{country}_{timestamp}.json', 'w') as outfile:
        json.dump(data, outfile)

def get_news(q, language='en', pageSize=100, apiKey=apiKey):
    URL = ('http://newsapi.org/v2/everything?'
        f'q={q}&'
        f'language={language}&'
        f'apiKey={apiKey}&'
        f'pageSize={pageSize}')
    data = requests.get(URL).json()
    timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M")
    titlestamp = qInTitle.lower().replace('and','-').replace('or','-').replace('not','not_').replace(' ','')
    with open(f'/home/msitapati/CryptoNews/news_data/{timestamp}_{titlestamp}.json', 'w') as outfile:
        json.dump(data, outfile)

def get_news_t(qInTitle, language='en', sortBy='publishedAt', pageSize=100, apiKey=apiKey):
    URL = ('http://newsapi.org/v2/everything?'
        f'qInTitle={qInTitle}&'
        f'language={language}&'
        f'sortBy={sortBy}&'
        f'pageSize={pageSize}&'
        f'apiKey={apiKey}')
    data = requests.get(URL).json()
    timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    titlestamp = qInTitle.lower().replace('and','-').replace('or','-').replace('not','not_').replace(' ','')
    with open(f'/home/msitapati/CryptoNews/news_data/{timestamp}_{titlestamp}.json', 'w') as outfile:
        json.dump(data, outfile)

def get_sources(country, apiKey=apiKey):
    URL = ('https://newsapi.org/v2/sources?'
        f'country={country}&'
        f'apiKey={apiKey}')
    data = requests.get(URL).json()
    timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M")
    with open(f'/home/msitapati/CryptoNews/data/SOURCES_{country}_{timestamp}.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
    qInTitle = input('Insert search-keyword: ')
    get_news_t(qInTitle)
    print(f'Created: NEWS_{qInTitle}')