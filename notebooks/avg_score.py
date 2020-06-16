import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd

df = pd.read_pickle('200604-192804-df_clean.pkl')

trace1 = go.Bar(x=df.index,
                y=df['CRY_score'],
                name = 'Crypto',
                marker=dict(color='#136dad'))

trace2 = go.Bar(x=df.index,
                y=df['BTC_score'],
                name = 'Bitcoin',
                marker=dict(color='#d4d12c'))

trace3 = go.Bar(x=df.index,
                y=df['ETH_score'],
                name = 'Ethereum',
                marker=dict(color='#4b5b75'))

data = [trace1, trace2, trace3]

layout = go.Layout(title='Average Score')

fig = go.Figure(data=data, layout=layout)
fig['layout']['yaxis'].update(range=[-1, 1], autorange=False)
fig.update_layout(xaxis_tickangle=-45)

pyo.plot(fig, filename='avg_score.html')
