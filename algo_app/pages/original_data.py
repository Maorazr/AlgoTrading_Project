

import dash
from dash import html, dcc, callback, Input, Output
from origin_data import origin_data
from getFiles import *
import plotly.graph_objects as go


dash.register_page(__name__)
global df
df = get_default_file('orig_data.csv', 'csv')

file_names = get_names('original_data')


layout = html.Div([
    dcc.Dropdown(
        id='selected-files-dropdown-original',
        options=file_names,
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
    Input('selected-files-dropdown-original', 'value')
)
def update_output(selected_file):
    if selected_file:
        file_path = f"original_data/{selected_file}"
        s3 = boto3.client('s3', aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key)
        obj = s3.get_object(Bucket=bucket_name, Key=file_path)
        global df
        df = pd.read_csv(obj['Body'])  # assuming the file is csv
        return f'You have selected: {selected_file}'
    else:
        return 'Please select a file'


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
