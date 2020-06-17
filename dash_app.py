#!/usr/bin/python3.7

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)

df_daily = pd.read_pickle('/home/msitapati/CryptoNews/df_data/df_daily.pkl')
df_daily = df_daily.fillna(0)
df = df_daily[:'2020-05-29']

colors = {
    'crypto': '#136dad',
    'bitcoin': '#d4d12c',
    'ethereum': '#4b5b75'}

initial_range = [df.index[13], df.index[0]+pd.DateOffset(1)]

app.layout = html.Div([
    html.H1('CryptoNews',
            style={'textAlign': 'center'}),

    dcc.Markdown('''
                    A project based on [Flask](https://stackshare.io/flask) and [Dash](https://plotly.com/dash). \n
                    The **ETL** collects the latest news about crypto from various news sources to a [MySQL](https://www.mysql.com/) database. \n
                    **Data Analysis** performs a sentiment analysis on headlines and description of articles, by using [vaderSentiment](https://pypi.org/project/vaderSentiment/). \n
                    Finally, this **Dashboard** displays the average sentiment score for the collected articles and how many were evaluated.

                '''),
html.Div([
    dcc.Graph(id='score-lines',
        figure = {'data':[
            go.Scatter(
                    x=df.index,
                    y=df['CRY_score'],
                    name = 'Crypto',
                    fill='tozeroy',
                    mode = 'lines',
                    marker=dict(color=colors['crypto'])),
            go.Scatter(
                    x=df.index,
                    y=df['BTC_score'],
                    name = 'Bitcoin',
                    fill='tozeroy',
                    mode = 'lines',
                    marker=dict(color=colors['bitcoin'])),
            go.Scatter(
                    x=df.index,
                    y=df['ETH_score'],
                    name = 'Ethereum',
                    fill='tozeroy',
                    mode = 'lines',
                    marker=dict(color=colors['ethereum']))],
                'layout': go.Layout(
                title = 'Daily Sentiment Score',
                yaxis = dict(title= 'Average Sentiment Score',
                             tickformat=".2%"),
                xaxis = dict(rangeselector=dict(buttons=list([dict(count=7,
                                                                 label="1w",
                                                                 step="day",
                                                                 stepmode="backward"),
                                                            dict(count=1,
                                                                 label="1m",
                                                                 step="month",
                                                                 stepmode="backward"),
                                                            dict(step="all")])),
                            rangeslider = dict(visible=False),
                            tickformat = '%a %d-%m',
                            type = "date",
                            range=initial_range))}),

    dcc.Graph(id='count-bars',
        figure={'data':[
            go.Bar(x=df.index,
                    y=df['crypto'],
                    name = 'Crypto',
                    marker=dict(color=colors['crypto']),
                    textposition='auto'),
            go.Bar(x=df.index,
                    y=df['bitcoin'],
                    name = 'Bitcoin',
                    marker=dict(color=colors['bitcoin']),
                    textposition='auto'),
            go.Bar(x=df.index,
                    y=df['ethereum'],
                    name = 'Ethereum',
                    marker=dict(color=colors['ethereum']),
                    textposition='auto')],
                'layout': go.Layout(
                title = 'Daily Articles Count',
                yaxis = {'title': 'Number of mentions in headline'},
                xaxis=dict(
                rangeselector=dict(buttons=list([dict(count=7,
                                                      label="1w",
                                                      step="day",
                                                      stepmode="backward"),
                                                 dict(count=1,
                                                      label="1m",
                                                      step="month",
                                                      stepmode="backward"),
                                                 dict(step="all")])),
                                rangeslider=dict(visible=False),
                                tickformat = '%a %d-%m',
                                type="date",
                                range=initial_range))}),
]),
html.Div([
    dcc.Markdown('''
                    A project by [Manohar Sitapati](https://www.linkedin.com/in/manoharsitapati/), find the whole original code in [GitHub](https://github.com/TheManohar/CryptoNews)
                '''),
])])