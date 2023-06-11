import dash
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
from temp import *
from getFiles import *
from res_data import *

dash.register_page(__name__)
results_df = get_default_file('0.1stop_res.csv', 'csv')

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
                 for ticker in results_df['Ticker'].unique()],
        value=results_df['Ticker'].unique()[0]
    ),
    dcc.Dropdown(
        id='strategy-selection',
        options=[{'label': s, 'value': s}
                 for s in results_df['Strategy'].unique()],
        value=results_df['Strategy'].unique()[0] if len(
            results_df['Strategy'].unique()) > 0 else None,
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
    html.Div(id='file-output')
])


def create_fig(ticker, selected_strategy="BB_RSI", selected_indicator=None):
    ticker_data = results_df[(results_df['Ticker'] == ticker) & (
        results_df['Strategy'] == selected_strategy)]
    entry_points = ticker_data[
        ((ticker_data['Actions'] == "OrderType.OPEN_LONG") | (ticker_data['Actions'] == "OrderType.OPEN_SHORT"))]
    exit_points = ticker_data[(ticker_data['Actions'] == '0')]
    fig = res_data(ticker_data, ticker, entry_points,
                   exit_points, selected_indicator)

    return fig


@callback(
    Output("stock-graph-results", "figure"),
    [Input("ticker-dropdown", "value"),
     Input("strategy-selection", "value"),
     Input('indicator-selection', 'value')])
def update_graph(ticker, selected_strategy, selected_indicator):
    return create_fig(ticker, selected_strategy, selected_indicator)
