

import dash
from dash import html, dcc, callback, Input, Output
from origin_data import origin_data
from getFiles import *
import plotly.graph_objects as go


dash.register_page(__name__)
global df
df = get_default_file('orig_data.csv', 'csv')

layout = html.Div([
    dcc.Dropdown(
        id='selected-files-dropdown',
        options=[],
        multi=False,
    ),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker}
                 for ticker in df['Ticker'].unique()],
        value=df['Ticker'].unique()[0]
    ),
    dcc.Graph(id='stock-graph-original',
              config={
                  'displayModeBar': False
              },
              figure={
                  'layout': go.Layout(
                      plot_bgcolor='rgba(255, 255, 255, 0.5)',
                      paper_bgcolor='rgba(255, 255, 255, 0.5)',
                      font={'color': 'black'},
                  )
              }
              ),
    html.Div(id='file-output')])


@callback(
    Output('file-output', 'children'),
    Input('selected-files-dropdown', 'value')
)
def update_output(selected_folder):
    if selected_folder:
        files = get_files_from_folder(selected_folder)
        files_dict = open_files_from_object(files)
        global df
        df = files_dict['orig_data.csv']
        return f'You have selected: {selected_folder}'
    else:
        return 'Please select a folder'


@callback(
    Output('stock-graph-original', 'figure'),
    [Input('ticker-dropdown', 'value'),
     Input('file-output', 'children')]
)
def update_graph(ticker, file_output):
    if ticker and file_output:

        ticker_data = df[df['Ticker'] == ticker]
        fig = origin_data(ticker_data, ticker)
        return fig
    else:
        return go.Figure()
