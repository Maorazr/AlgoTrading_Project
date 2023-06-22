
# import dash
# from dash import html, dcc, Input, Output, callback
# import plotly.graph_objects as go
# from temp import *
# from getFiles import *
# from res_data import *


# dash.register_page(__name__)
# global df
# global results_df
# global file_names

# file_names = get_names('backtesting_results')
# results_df = get_default_file('backtesting_results/2010_2019_0.25sl_results.csv', 'csv')
# df = results_df

# layout = html.Div([
#     dcc.Dropdown(
#         id='selected-files-dropdown-results',
#         options=file_names,
#         multi=False,
#     ),
#     dcc.Dropdown(
#         id='indicator-selection',
#         options=[
#             {'label': 'RSI', 'value': 'RSI'},
#             {'label': 'CCI', 'value': 'CCI'},
#             {'label': 'Volume', 'value': 'Volume'}
#         ],
#         value=['RSI', 'CCI', 'Volume'],
#         multi=True,
#         placeholder='Select indicators',
#         style={'display': 'block'}
#     ),
#     dcc.Dropdown(
#         id='ticker-dropdown',
#         options=[{'label': ticker, 'value': ticker}
#                  for ticker in df['Ticker'].unique()],
#         value=df['Ticker'].unique()[0]
#     ),
#     dcc.Dropdown(
#         id='strategy-selection',
#         options=[{'label': 'Boillnger bound + RSI', 'value': 'BB_RSI'},
#                  {'label': 'Boillnger bound + CCI', 'value': 'BB_CCI'},
#                  {'label': 'Buy & Hold', 'value': 'B&H'}],
#         value='BB_RSI',
#         placeholder='Select a strategy',
#         multi=False,
#     ),
#     dcc.Graph(id='stock-graph-results',
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
#     html.Button('Refresh', id='refresh-button-results', n_clicks=0),
#     html.Div(id='file-output-results'),
# ])


# def calcualte_dtick():
#     global df
#     days = len(df['Date'].unique())
#     years = days / 255
#     if years <= 10:
#         dtick = 'M3'
#     elif years <= 20:
#         dtick = 'M7'
#     else:
#         dtick = 'M12'
#     return dtick


# def create_fig(ticker, selected_strategy="BB_RSI", selected_indicator=None):
#     global df
#     dtick = calcualte_dtick()
#     ticker_data = df[(df['Ticker'] == ticker) & (
#         df['Strategy'] == selected_strategy)]
#     entry_points = ticker_data[
#         ((ticker_data['Actions'] == "OrderType.OPEN_LONG") | (ticker_data['Actions'] == "OrderType.OPEN_SHORT"))]
#     exit_points = ticker_data[(ticker_data['Actions'] == '0')]
#     fig = res_data(ticker_data, ticker, entry_points,
#                    exit_points, selected_indicator)

#     fig.update_layout(
#         xaxis=dict(
#             tickmode='linear',
#             tick0=df['Date'][0],
#             dtick=dtick,
#         )
#     )

#     return fig


# @callback(
#     Output('file-output-results', 'children'),
#     Output('ticker-dropdown', 'options'),
#     Input('selected-files-dropdown-results', 'value')
# )
# def update_output(selected_file):
#     global df

#     if selected_file:
#         file_path = f"backtesting_results/{selected_file}"
#         obj = s3_client.get_object(Bucket=bucket_name, Key=file_path)
#         df = pd.read_csv(obj['Body'])  # assuming the file is csv
#         return f'You have selected: {selected_file}', [{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()]
#     else:

#         return 'Please select a file', []


# @callback(
#     Output("stock-graph-results", "figure"),
#     [Input("ticker-dropdown", "value"),
#      Input("strategy-selection", "value"),
#      Input('indicator-selection', 'value'),
#      Input('file-output-results', 'children')])
# def update_graph(ticker, selected_strategy, selected_indicator, file_output_results):
#     return create_fig(ticker, selected_strategy, selected_indicator)


# @callback(
#     Output('selected-files-dropdown-results', 'options'),
#     [Input('refresh-button-results', 'n_clicks')]
# )
# def update_file_list(n_clicks):
#     if n_clicks is not None:
#         file_names = get_names('backtesting_results')
#         return file_names



import dash
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
from temp import *
from getFiles import *
from res_data import *


dash.register_page(__name__)

results_df = get_default_file('backtesting_results/2010_2019_0.25sl_results.csv', 'csv')
df = results_df

layout = html.Div([
    dcc.Dropdown(
        id='indicator-selection',
        options=[
            {'label': 'RSI', 'value': 'RSI'},
            {'label': 'CCI', 'value': 'CCI'},
            {'label': 'Volume', 'value': 'Volume'}
        ],
        value=['RSI', 'CCI', 'Volume'],
        multi=True,
        placeholder='Select indicators',
        style={'display': 'block'}
    ),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker}
                 for ticker in df['Ticker'].unique()],
        value=df['Ticker'].unique()[0]
    ),
    dcc.Dropdown(
        id='strategy-selection',
        options=[{'label': 'Boillnger bound + RSI', 'value': 'BB_RSI'},
                 {'label': 'Boillnger bound + CCI', 'value': 'BB_CCI'},
                 {'label': 'Buy & Hold', 'value': 'B&H'}],
        value='BB_RSI',
        placeholder='Select a strategy',
        multi=False,
    ),
    dcc.Graph(id='stock-graph-results',
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


def calcualte_dtick():
    days = len(df['Date'].unique())
    years = days / 255
    if years <= 10:
        dtick = 'M3'
    elif years <= 20:
        dtick = 'M7'
    else:
        dtick = 'M12'
    return dtick


def create_fig(ticker, selected_strategy="BB_RSI", selected_indicator=None):
    dtick = calcualte_dtick()
    ticker_data = df[(df['Ticker'] == ticker) & (
        df['Strategy'] == selected_strategy)]
    entry_points = ticker_data[
        ((ticker_data['Actions'] == "OrderType.OPEN_LONG") | (ticker_data['Actions'] == "OrderType.OPEN_SHORT"))]
    exit_points = ticker_data[(ticker_data['Actions'] == '0')]
    fig = res_data(ticker_data, ticker, entry_points,
                   exit_points, selected_indicator)

    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            tick0=df['Date'][0],
            dtick=dtick,
        )
    )

    return fig


@callback(
    Output("stock-graph-results", "figure"),
    [Input("ticker-dropdown", "value"),
     Input("strategy-selection", "value"),
     Input('indicator-selection', 'value')]
)
def update_graph(ticker, selected_strategy, selected_indicator):
    return create_fig(ticker, selected_strategy, selected_indicator)
