#!/usr/bin/python3.7

import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import warnings

df = pd.read_pickle('/home/msitapati/CryptoNews/df_data/df_articles.pkl')
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
df_clean['description'] = df_clean['description'].str.replace('…','')

## Clean df content field
df_clean['content'] = df['content'].str.split('…', expand=True)[0]

# Sentiment Analysis
analyzer = SentimentIntensityAnalyzer()

## Create t_score
df_clean['title'] = df_clean['title'].replace(np.NaN, ' ')
df_clean['t_score'] = [i['compound'] for i in df_clean['title'].apply(analyzer.polarity_scores)]
df_clean['t_score'] = df_clean['t_score'].replace(0, np.NaN)

## Create d_score
df_clean['description'] = df_clean['description'].replace(np.NaN, ' ')
df_clean['d_score'] = [i['compound'] for i in df_clean['description'].apply(analyzer.polarity_scores)]
df_clean['d_score'] = df_clean['d_score'].replace(0, np.NaN)

## Create c_score
df_clean['content'] = df_clean['content'].replace(np.NaN, ' ')
df_clean['c_score'] = [i['compound'] for i in df_clean['content'].apply(analyzer.polarity_scores)]
df_clean['c_score'] = df_clean['c_score'].replace(0, np.NaN)

## Avreage Score
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    df_clean['avg_score'] = np.nanmean(df_clean[['t_score', 'd_score', 'c_score']], axis=1)
df_clean = df_clean.replace(np.NaN, 0)

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

df_clean.name = 'df_clean'
df_daily.name = 'df_daily'

def get_df_clean(df_clean=df_clean):
    return df_clean

def get_df_daily(df_daily=df_daily):
    return df_daily

def save_dash_df(df):
    return df.to_pickle(f'/home/msitapati/CryptoNews/df_data/{df.name}.pkl')

if __name__ == "__main__":
    save_dash_df(df_daily)
    print(f'CREATED: {df_daily.name}.pkl')