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

app.layout = html.Div([
    html.H1('CryptoNews',
            style={'textAlign': 'center'}),

    html.Div('An API based on Flask. It collects and displays the latest news about cryptocurrency from various news sources.',
             style={'textAlign': 'center'}),

    dcc.Graph(id='score-lines',
        figure = {'data':[
            go.Scatter(
                    x=df.index,
                    y=df['CRY_score'],
                    name = 'Crypto',
                    fill='tozeroy',
                    mode = 'lines+markers',
                    marker=dict(color=colors['crypto'])),
            go.Scatter(
                    x=df.index,
                    y=df['BTC_score'],
                    name = 'Bitcoin',
                    fill='tozeroy',
                    mode = 'lines+markers',
                    marker=dict(color=colors['bitcoin'])),
            go.Scatter(
                    x=df.index,
                    y=df['ETH_score'],
                    name = 'Ethereum',
                    fill='tozeroy',
                    mode = 'lines+markers',
                    marker=dict(color=colors['ethereum']))],
                'layout': go.Layout(
                title = 'Daily Sentiment Score',
                yaxis = {'title': 'Average Sentiment Score'},
                xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=8,
                             label="1w",
                             step="day",
                             stepmode="backward"),
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=False
                ),
                type="date"))}),

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
                rangeselector=dict(
                    buttons=list([
                        dict(count=8,
                             label="1w",
                             step="day",
                             stepmode="backward"),
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=False
                ),
                type="date"))}),

])