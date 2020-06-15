#!/usr/bin/python3.7

import pandas as pd
import datetime
import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_pickle('df_data/df_articles.pkl')
df = df.set_index(['publishedAt'])

# Data Ceaning
## Create keyword-check columns
df_clean = df.copy()
df_clean.name = 'df_clean'
df_clean['crypto'] = df_clean['title'].str.contains('crypto', case=False)
df_clean['bitcoin'] = df_clean['title'].str.contains('bitcoin', case=False)
df_clean['ethereum'] = df_clean['title'].str.contains('ethereum', case=False)

## Clean df author field
df_clean['author'] = df['author'].str.split(',', expand=True)[0]
df_clean['author'] = df_clean['author'].str.replace('Cointelegraph By ','')
df_clean['author'] = df_clean['author'].str.replace(')','')
df_clean['author'] = df_clean['author'].str.split('(', expand=True)[0]

## Clean df description field
for i,v in enumerate(df_clean['description']):
    if str(v).endswith('…'):
        df_clean['description'][i] = v[:-1]
        
## Clean df content field
for i,v in enumerate(df_clean['content']):
    if str(v).endswith(' chars]'):
        df_clean['content'][i] = v[:-16]


# Sentiment Analysis
analyzer = SentimentIntensityAnalyzer()

## Title  Sentiment Analysis
df_clean['t_score'] = pd.Series()
for i,v in enumerate(df_clean['title']):
    vs = analyzer.polarity_scores(v)
    df_clean['t_score'][i] = vs['compound'] 

## Description Sentiment Analysis
df_clean['d_score'] = pd.Series(dtype='float')
for i,v in enumerate(df_clean['description']):
    try:
        vs = analyzer.polarity_scores(v)
        df_clean['d_score'][i] = vs['compound']
    except:
        df_clean['d_score'][i] = 0

## Content Sentiment Analysis
df_clean['c_score'] = pd.Series()
for i,v in enumerate(df_clean['content']):
    try:
        vs = analyzer.polarity_scores(v)
        df_clean['c_score'][i] = vs['compound']
    except:
        df_clean['c_score'][i] = 0

## Avreage Score
df_clean['avg_score'] = (df_clean['t_score'] + df_clean['d_score'] + df_clean['c_score']) / 3
    

# Create df_daily
df_daily = df_clean[['crypto','bitcoin','ethereum']]
df_daily = df_daily.resample('D').sum()
df_daily = df_daily.sort_index(ascending=False)

## Daily Crypto Count 
CRY_score = pd.DataFrame(df_clean.loc[(df_clean['crypto']==True) & (df_clean['avg_score']!=0)]['avg_score'])
CRY_score = CRY_score.resample('D').mean()
CRY_score = CRY_score.sort_index(ascending=True)
df_daily['CRY_score'] = df_daily.merge(CRY_score, how='outer', on='publishedAt')['avg_score']

## Daily Bitcoin Count 
BTC_score = pd.DataFrame(df_clean.loc[(df_clean['bitcoin']==True) & (df_clean['avg_score']!=0)]['avg_score'])
BTC_score = BTC_score.resample('D').mean()
BTC_score = BTC_score.sort_index(ascending=True)
df_daily['BTC_score'] = df_daily.merge(BTC_score, how='outer', on='publishedAt')['avg_score']

## Daily Ethereum Count 
ETH_score = pd.DataFrame(df_clean.loc[(df_clean['ethereum']==True) & (df_clean['avg_score']!=0)]['avg_score'])
ETH_score = ETH_score.resample('D').mean()
ETH_score = ETH_score.sort_index(ascending=True)
df_daily['ETH_score'] = df_daily.merge(ETH_score, how='outer', on='publishedAt')['avg_score']

df_daily.name = 'df_daily'

def save_df(df):
    return df.to_pickle(f'df_data/{df.name}.pkl')

if __name__ == "__main__":
    save_df(df_clean)
    print(f'CREATED: {df_clean.name}.plk')
    save_df(df_daily)
    print(f'CREATED: {df_daily.name}.plk')