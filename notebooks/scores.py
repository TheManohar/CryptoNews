import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_pickle('200604-192804-df_clean.pkl')


app.layout = html.Div([
    dcc.Graph(
        id='t_score-vs-d_score',
        figure={
            'data': [
                dict(
                    x=df[df['source_id'] == i]['t_score'],
                    y=df[df['source_id'] == i]['d_score'],
                    text=df[df['source_id'] == i]['source'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.source_id.unique()
            ],
            'layout': dict(
                xaxis={'type': 'log', 'title': 'Title Score'},
                yaxis={'title': 'Description Score'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)