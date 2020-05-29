#!/usr/bin/python3.7

import json
import os
import sys

def read_data():
    data = []
    for filename in os.listdir(os.getcwd()+'/news_data')[:100]:
        try:
            with open(os.path.join(os.getcwd()+'/news_data', filename), 'r') as f:
                data.append(json.load(f))
        except:
            e = sys.exc_info()[0]
            print(f'Error: {filename} {e}')
        finally:
            os.replace(f'{os.getcwd()}/news_data/{filename}', f'{os.getcwd()}/done/{filename}')
    return data

def parse_data(data):
    parsed_data = []
    for element in data:
        for i,v in enumerate(element["articles"]):
            source = v['source']['name']
            source_id = v['source']['id']
            if source_id is None:
                source_id = source.lower().replace(' ','-')
            author = v["author"]
            title = v["title"]
            description = v["description"]
            url = v["url"]
            publishedAt = ' '.join(v["publishedAt"].replace('Z','').split('T'))
            content = v["content"]
            row = publishedAt, source, source_id, author, title, description, content, url
            parsed_data.append(row)
    return parsed_data

if __name__ == "__main__":
    data = read_data()
    parsed_data = parse_data(data)
    print(parsed_data)