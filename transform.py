#!/usr/bin/python3.7

import json
import os
import sys

def read_data():
    data = []
    for filename in os.listdir('/home/msitapati/CryptoNews/news_data'):
        if filename.endswith(".json"):
            try:
                with open(os.path.join('/home/msitapati/CryptoNews/news_data', filename), 'r') as f:
                    data.append(json.load(f))
            except:
                e = sys.exc_info()[0]
                print(f'Error: {filename} {e}')
            finally:
                #os.replace(f'{os.getcwd()}/news_data/{filename}', f'{os.getcwd()}/done/{filename}')
                os.remove(f'/home/msitapati/CryptoNews/news_data/{filename}')
    return data

def parse_data(data):
    parsed_data = []
    for element in data:
        for article in element["articles"]:
            source = article['source']['name']
            source_id = article['source']['id']
            if source_id is None:
                source_id = source.lower().replace(' ','-')
            author = article["author"]
            title = article["title"]
            description = article["description"]
            url = article["url"]
            publishedAt = ' '.join(article["publishedAt"].replace('Z','').split('T'))
            content = article["content"]
            row = publishedAt, source, source_id, author, title, description, content, url
            parsed_data.append(row)
    return parsed_data