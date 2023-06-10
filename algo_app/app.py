

from io import StringIO, BytesIO
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from botocore.exceptions import NoCredentialsError
import json
import boto3
from temp import *
from stats_data import *
from origin_data import *
from res_data import *
from getFiles import *
app = Dash(__name__)
server = app.server


bucket_name = 'algotradingproject'
s3 = boto3.client('s3',
                  aws_access_key_id='AKIA4C5ZLMSXGT5GGTTU',
                  aws_secret_access_key='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'
                  )

data_file_key = 'orig_data.csv'
# 2015_2019_optimized_params.csv
results_file_key = '0.1stop_res.csv'
# 2015_2019_optimized_params_0.1stop_res.csv
stats_file_key = '0.1stop_stats.json'
# 2015_2019_optimized_params_0.1stop_stats_final.json
stat2_file_key = '2015_2019_default_params_0.1stop_stats_final.json'

csv_obj = s3.get_object(Bucket=bucket_name, Key=data_file_key)
csv_data = csv_obj['Body'].read().decode('utf-8')
df = pd.read_csv(StringIO(csv_data), parse_dates=['Date'])

# Read results CSV file from S3
results_csv_obj = s3.get_object(Bucket=bucket_name, Key=results_file_key)
results_csv_data = results_csv_obj['Body'].read().decode('utf-8')
results_df = pd.read_csv(StringIO(results_csv_data), parse_dates=['Date'])

# Read strategy_summaries JSON file from S3
strategy_summaries_json_obj = s3.get_object(
    Bucket=bucket_name, Key=stats_file_key)
strategy_summaries_json_data = strategy_summaries_json_obj['Body'].read(
).decode('utf-8')
strategy_summaries = json.loads(strategy_summaries_json_data)

# Read strategy_summaries2 JSON file from S3
strategy_summaries2_json_obj = s3.get_object(
    Bucket=bucket_name, Key=stat2_file_key)
strategy_summaries2_json_data = strategy_summaries2_json_obj['Body'].read(
).decode('utf-8')
strategy_summaries2 = json.loads(strategy_summaries2_json_data)


sma_column = find_sma_column(results_df)
bucket_contents = [{'label': name, 'value': name}
                   for name in list_files_in_bucket()]

files = {}


@app.callback(
    Output('file-output', 'children'),
    Input('selected-files-dropdown', 'value')
)
def update_output(selected_folder):
    if selected_folder:
        files = get_files_from_folder(selected_folder)
        return f'You have selected: {selected_folder}'
    else:
        return 'Please select a folder'


app.layout = html.Div([
    dcc.Dropdown(
        id='selected-files-dropdown',
        options=bucket_contents,
        multi=False,
    ),
    dcc.Dropdown(
        id='data-type-dropdown',
        options=[{'label': data_type, 'value': data_type}
                 for data_type in ['Original Data', 'Results Data', 'Stats']],
        value='Original Data'
    ),
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
        style={'display': 'none'}
    ),

    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker}
                 for ticker in df['Ticker'].unique()],
        value=df['Ticker'].unique()[0]
    ),
    dcc.Dropdown(
        id='strategy-selection',
        options=[{'label': s, 'value': s}
                 for s in results_df['Strategy'].unique()],
        value=results_df['Strategy'].unique()[0] if len(
            results_df['Strategy'].unique()) > 0 else None,
        placeholder='Select a strategy',
        multi=False,
        style={'display': 'none'}
    ),
    dcc.Graph(id='stock-graph',
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
    # html.Div([
    #     html.Label("Start Date:"),
    #     dcc.Input(id='start-date', type='text', placeholder='YYYY-MM-DD'),
    #     html.Label("End Date:"),
    #     dcc.Input(id='end-date', type='text', placeholder='YYYY-MM-DD'),
    #     html.Button('Apply Date Range', id='apply-date-range', n_clicks=0),
    # ]),
])


def create_fig(data_type, ticker, selected_strategy="BB_RSI", selected_indicator=None):
    if data_type == 'Original Data':
        ticker_data = df[df['Ticker'] == ticker]
        fig = origin_data(ticker_data, ticker)
    elif data_type == 'Results Data':
        ticker_data = results_df[(results_df['Ticker'] == ticker) & (
            results_df['Strategy'] == selected_strategy)]
        entry_points = ticker_data[
            ((ticker_data['Actions'] == "OrderType.OPEN_LONG") | (ticker_data['Actions'] == "OrderType.OPEN_SHORT"))]
        exit_points = ticker_data[(ticker_data['Actions'] == '0')]
        fig = res_data(ticker_data, ticker, entry_points,
                       exit_points, selected_indicator)
    elif data_type == 'Stats':
        fig = stats_data(ticker)
    else:
        raise ValueError(f"Invalid data_type: {data_type}")

    return fig


@app.callback(
    Output("stock-graph", "figure"),
    [Input("data-type-dropdown", "value"),
     Input("ticker-dropdown", "value"),
     Input("strategy-selection", "value")],
    Input('indicator-selection', 'value'))
#  Input("apply-date-range", "n_clicks")],
# [State('start-date', 'value'),
#  State('end-date', 'value')],
def update_graph(data_type, ticker, selected_strategy, selected_indicator):
    if data_type == 'Results Data':
        return create_fig(data_type, ticker, selected_strategy, selected_indicator)
    else:
        return create_fig(data_type, ticker, selected_strategy)
# def update_graph(data_type, ticker, selected_strategy, n_clicks, start_date, end_date, selected_indicator):
#     if data_type == 'Results Data':
#         return create_fig(data_type, ticker, start_date, end_date, selected_strategy, selected_indicator)
#     else:
#         return create_fig(data_type, ticker, start_date, end_date, selected_strategy)


@app.callback(
    Output('strategy-selection', 'style'),
    [Input('data-type-dropdown', 'value')]
)
def update_strategy_dropdown_visibility(data_type):
    if data_type == 'Results Data':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('indicator-selection', 'style'),
    [Input('data-type-dropdown', 'value')]
)
def update_indicator_dropdown_visibility(data_type):
    if data_type == 'Results Data':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


def update_stats(data_type, ticker):
    if data_type == 'Stats':
        return create_fig(data_type, ticker)
    else:
        return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)
