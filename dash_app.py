#!/usr/bin/python3.7

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
#from plotly.subplots import make_subplots
import pandas as pd
import dash_table
import os
import dash_bootstrap_components as dbc
from datetime import datetime as dt

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

my_path = os.path.abspath(os.path.dirname(__file__))
path = f'{my_path}/df_data/df_clean.pkl'
df_daily = pd.read_pickle(f'{path}')
#df_daily = df_daily.fillna(0)
df = df_daily['2020-05-29':]
df['date'] = df.index.strftime('%x, %X')
df['avg_score'] = round(df['avg_score'], 2)

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1('CryptoNews'),
                dcc.Markdown('An interactive dashboard by [Manohar Sitapati](https://www.linkedin.com/in/manoharsitapati/).'),
                dcc.Markdown('Detailed documentation and code are available on [GitHub](https://github.com/TheManohar/CryptoNews#readme).')
            ], style={'padding':10}),
            html.Div([
                html.H3('Pick a Keyword'),
                dcc.Dropdown(
                    id='coin-selector',
                    options=[
                        {'label': 'Crypto', 'value': 'crypto'},
                        {'label': 'Bitcoin', 'value': 'bitcoin'},
                        {'label': 'Ethereum', 'value': 'ethereum'}
                    ],
                    value='bitcoin',
                    clearable=False
                )
            ], style={'padding':10}),
            html.Div([
                html.H3('Pick a Date Range'),
                dcc.DatePickerRange(
                    id='date-picker',
                    min_date_allowed=dt(2020, 5, 29),
                    initial_visible_month=dt.today(),
                    first_day_of_week=1
                )
            ], style={'padding':10})
        ], width=3),
        dbc.Col([
            html.Div([
                dcc.Graph(
                    id='graph-1',
                    config={'displayModeBar':False}
                )
            ],
            style={'padding':10}
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dash_table.DataTable(
                    id='table-1',
                    columns=[
                        {'name': 'Date', 'id': 'date'},
                        {'name': 'Source', 'id': 'source'},
                        {'name': 'Title', 'id': 'title'},
                        {'name': 'Description', 'id': 'description'},
                        {'name': 'Score', 'id': 'avg_score'}
                    ],
                    style_cell={
                        'textAlign': 'left',
                        'padding': '5px',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'textOverflow': 'ellipsis',
                        'overflow': 'hidden',
                        'maxWidth': '800px'
                    },
                    style_cell_conditional=[
                        {'if': {'column_id': 'title'},
                        'maxWidth': '600px'},
                        {'if': {'column_id': 'description'},
                        'maxWidth': '800px'},
                    ],
                    sort_by=[{'column_id':'date', 'direction':'desc'}],
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    page_action="native",
                    page_current= 0,
                    page_size= 10
                )
            ])
        ])
    ], style={'padding-left':40, 'padding-right':40})
])

@app.callback(
    Output('graph-1', 'figure'),
    [Input('coin-selector', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')
    ])
def update_graph(coin, start_date, end_date):
    dff = df[df[str(coin)] == True]
    dff = dff[start_date:end_date]
    dff_as = pd.DataFrame()
    dff_as['avg_score'] = dff['avg_score'].resample('H').mean()
    dff_as['mvn_avg'] = dff_as['avg_score'].rolling('12h').mean()
    dff_as.fillna(0, inplace=True)
    dff_as = round(dff_as,2)
    dff_ac = pd.DataFrame()
    dff_ac['count'] = dff[str(coin)].resample('H').sum()
    dff_ac.fillna(0, inplace=True)
    bins=[0,1,2,3,99]
    colors=['tomato', 'orange', 'gold', 'lightgreen']
    dff_ac['color'] = pd.cut(dff_ac['count'], bins=bins, labels=colors)

    return {
        'data': [
            go.Scatter(
                name=' Hourly Score',
                x=dff_as.index,
                y=dff_as['avg_score'],
                mode='lines',
                opacity=0.8,
                line=dict(
                    color='midnightblue',
                    width=1
                )
            ),
            go.Scatter(
                name='Moving Average',
                x=dff_as.index,
                y=dff_as['mvn_avg'],
                mode='lines',
                fill='tozeroy',
                opacity=0.8,
                line=dict(
                    color='darkorange',
                    width=2
                )
            ),
            go.Bar(
                name = 'Article Count',
                x=dff_ac.index,
                y=dff_ac['count'],
                yaxis='y2',
                opacity=0.5,
                marker=dict(
                    color=dff_ac['color']
                )
            )
        ],
        'layout': go.Layout(
            legend=dict(
                orientation='h',
                x=-0,
                y=1.1
                ),
            yaxis = dict(
                #tickformat=".2%",
                showticklabels=False,
                rangemode='tozero',
                range=[-1, 1],
                showgrid=False
                ),
            yaxis2 = dict(
                overlaying='y',
                side='right',
                rangemode='tozero',
                range=[0, 50],
                showgrid=False,
                ),
            xaxis = dict(
                showgrid=True,
                rangeselector=dict(
                    buttons=list([
                        dict(
                            count=24,
                            label="24h",
                            step="hour",
                            stepmode="backward"
                        ),
                        dict(
                            count=7,
                            label="1w",
                            step="day",
                            stepmode="backward"
                        ),
                        dict(
                            count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"
                        ),
                        dict(
                            step="all"
                        )
                    ])
                ),
                rangeslider = dict(
                    visible=True,
                    borderwidth=1,
                    thickness=0.01
                    ),
                tickformat = '%a %d-%m <br> %H:%M',
                type = "date",
                range=[df.index[-1]-pd.DateOffset(30), df.index[-1]]
            ),
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            dragmode= 'pan'
        )
    }

@app.callback(
    Output('table-1', 'data'),
    [Input('coin-selector', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')
    ])
def update_table(coin, start_date, end_date):
    dff = df[df[str(coin)] == True]
    dff = dff[start_date:end_date]
    return dff.to_dict('records')