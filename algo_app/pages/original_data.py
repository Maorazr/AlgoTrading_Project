# import dash
# from dash import html, dcc, callback, Input, Output
# from origin_data import origin_data
# from getFiles import *
# import plotly.graph_objects as go

# dash.register_page(__name__)

# default_df = get_default_file('original_data/2010_2019_Processed.csv', 'csv')
# file_names = get_names('original_data')

# layout = html.Div([
#     dcc.Dropdown(
#         id='selected-files-dropdown-original',
#         options=file_names,
#         multi=False,
#     ),
#     dcc.Dropdown(
#         id='ticker-dropdown-orig',
#         options=[{'label': ticker, 'value': ticker}
#                  for ticker in default_df['Ticker'].unique()],
#         value=default_df['Ticker'].unique()[0]
#     ),
#     html.Button('Refresh', id='refresh-button-original', n_clicks=0),
#     dcc.Graph(id='stock-graph-original',
#               config={
#                   'displayModeBar': False
#               },
#               figure={
#                   'layout': go.Layout(
#                       plot_bgcolor='rgba(255, 255, 255, 0.5)',
#                       paper_bgcolor='rgba(255, 255, 255, 0.5)',
#                       font={'color': 'black'},
#                   )
#               }
#               ),
#     html.Div(id='file-output'),
# ])


# @callback(
#     Output('file-output', 'children'),
#     Output('ticker-dropdown-orig', 'options'),
#     Input('selected-files-dropdown-original', 'value')
# )
# def update_output(selected_file):
#     if selected_file:
#         file_path = f"original_data/{selected_file}"
#         obj = s3_client.get_object(Bucket=bucket_name, Key=file_path)
#         df = pd.read_csv(obj['Body'])  # assuming the file is csv
#         return f'You have selected: {selected_file}', [{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()]
#     else:
#         return dash.no_update, dash.no_update


# @callback(
#     Output('stock-graph-original', 'figure'),
#     Input('ticker-dropdown-orig', 'value'),
#     Input('selected-files-dropdown-original', 'value'),
# )
# def update_graph(ticker, selected_file):
#     if ticker and selected_file:
#         file_path = f"original_data/{selected_file}"
#         obj = s3_client.get_object(Bucket=bucket_name, Key=file_path)
#         df = pd.read_csv(obj['Body'])
#         ticker_data = df[df['Ticker'] == ticker]
#         fig = origin_data(ticker_data, ticker)
#         return fig
#     else:
#         return go.Figure()


# @callback(
#     Output('selected-files-dropdown-original', 'options'),
#     [Input('refresh-button-original', 'n_clicks')]
# )
# def update_file_list(n_clicks):
#     if n_clicks is not None:
#         # Replace this with your actual code to get the updated file list
#         file_names = get_names('original_data')
#         return file_names


import dash
from dash import html, dcc, callback, Input, Output
from origin_data import origin_data
from getFiles import *
import plotly.graph_objects as go

dash.register_page(__name__)

default_df = get_default_file('original_data/2010_2019_Processed.csv', 'csv')

layout = html.Div([
    dcc.Dropdown(
        id='ticker-dropdown-orig',
        options=[{'label': ticker, 'value': ticker}
                 for ticker in default_df['Ticker'].unique()],
        value=default_df['Ticker'].unique()[0]
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
])

@callback(
    Output('stock-graph-original', 'figure'),
    Input('ticker-dropdown-orig', 'value')
)
def update_graph(ticker):
    if ticker:
        ticker_data = default_df[default_df['Ticker'] == ticker]
        fig = origin_data(ticker_data, ticker)
        return fig
    else:
        return go.Figure()
