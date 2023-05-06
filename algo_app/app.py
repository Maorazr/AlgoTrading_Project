from io import StringIO
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import json
import boto3

app = Dash(__name__)
server = app.server

bucket_name = 'algotradingproject'
s3 = boto3.client('s3')
data_file_key = '2015_2019_optimized_params.csv'
results_file_key = '2015_2019_optimized_params_0.1stop_res.csv'
stats_file_key = '2015_2019_optimized_params_0.1stop_stats_final.json'
stat2_file_key = '2015_2019_default_params_0.1stop_stats_final.json'

# stats_file_key = '2015_2019_optimized_params_0.1stop_stats.json'
# stat2_file_key = '2015_2019_default_params_0.1stop_stats.json'


csv_obj = s3.get_object(Bucket=bucket_name, Key=data_file_key)
csv_data = csv_obj['Body'].read().decode('utf-8')
df = pd.read_csv(StringIO(csv_data), parse_dates=['Date'])

# Read results CSV file from S3
results_csv_obj = s3.get_object(Bucket=bucket_name, Key=results_file_key)
results_csv_data = results_csv_obj['Body'].read().decode('utf-8')
results_df = pd.read_csv(StringIO(results_csv_data), parse_dates=['Date'])

# Read strategy_summaries JSON file from S3
strategy_summaries_json_obj = s3.get_object(Bucket=bucket_name, Key=stats_file_key)
strategy_summaries_json_data = strategy_summaries_json_obj['Body'].read().decode('utf-8')
strategy_summaries = json.loads(strategy_summaries_json_data)

# Read strategy_summaries2 JSON file from S3
strategy_summaries2_json_obj = s3.get_object(Bucket=bucket_name, Key=stat2_file_key)
strategy_summaries2_json_data = strategy_summaries2_json_obj['Body'].read().decode('utf-8')
strategy_summaries2 = json.loads(strategy_summaries2_json_data)

# df = pd.read_csv('Data/Processed/2015-01_2019-12_[14,14,10,0.015,10]_data.csv', parse_dates=['Date'])  # replace with your actual data file
# results_df = pd.read_csv('results/2015-01_2019-12_[14,14,10,0.015,10]_0.1stop_62-38_res.csv', parse_dates=['Date'])
# with open('results/Json_stat/2015-01_2019-12_[14,14,10,0.015,10]_0.1stop_62-38_stats.json', 'r') as f1:
#     strategy_summaries = json.load(f1)
# with open('results/Json_stat/2015-01_2019-12_[20,20,20,0.015,14]_0.1stop_70_30_stats.json', 'r') as f2:
#     strategy_summaries2 = json.load(f2)

sma_column = None


def find_sma_column(ticker_data):
    global sma_column
    for col_name in ticker_data.columns:
        if col_name.startswith('SMA_'):
            sma_column = col_name
            break


find_sma_column(results_df)


def generate_rows(ticker, strategy_summaries):
    ticker_strategy_keys = [key for key in strategy_summaries.keys() if key.startswith(ticker)]
    strategy_results = {key: strategy_summaries[key] for key in ticker_strategy_keys}
    rows = []
    for strategy_name, summary in strategy_results.items():
        if not summary:  # Skip if the summary is empty
            continue

        row = {
            'Strategy': strategy_name,
            'Total return': summary['Total return'],
            'Sharpe': summary['Sharpe'],
            # 'Sortino': summary['Sortino'],
            # 'Max balance drawdown': summary['Max balance drawdown'],
            'Max drawdown': summary['Max drawdown'],
            'Returns std': summary['Returns std'],
            'Downside deviation': summary['Downside deviation'],
            'Best trade': summary['Best trade'],
            'Worst trade': summary['Worst trade'],
            'Positive trades': summary['Positive trades'],
            'Positive trading days': summary['Positive trading days'],
        }
        rows.append(row)

    return rows


app.layout = html.Div([
    dcc.Dropdown(
        id='data-type-dropdown',
        options=[{'label': data_type, 'value': data_type} for data_type in ['Original Data', 'Results Data', 'Stats']],
        value='Original Data'
    ),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
        value=df['Ticker'].unique()[0]
    ),
    dcc.Dropdown(
        id='strategy-selection',
        options=[{'label': s, 'value': s} for s in results_df['Strategy'].unique()],
        value=results_df['Strategy'].unique()[0] if len(results_df['Strategy'].unique()) > 0 else None,
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
    html.Div([
        html.Label("Start Date:"),
        dcc.Input(id='start-date', type='text', placeholder='YYYY-MM-DD'),
        html.Label("End Date:"),
        dcc.Input(id='end-date', type='text', placeholder='YYYY-MM-DD'),
        html.Button('Apply Date Range', id='apply-date-range', n_clicks=0),
    ]),
    # html.Div(id='stats-container', children=[dcc.Graph(id='stats')])

])


def common_traces(ticker_data, ticker, fig):
    fig.add_trace(
        go.Scatter(x=ticker_data['Date'], y=ticker_data['BU'], line=dict(color='green'), name='BU', yaxis='y1'))
    fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BL'], line=dict(color='red'), name='BL', yaxis='y1'))
    fig.add_trace(
        go.Scatter(x=ticker_data['Date'], y=ticker_data[sma_column], line=dict(color='orange'), name=sma_column,
                   yaxis='y1'))
    fig.add_trace(
        go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line=dict(color='blue'), name='RSI', yaxis='y2'))
    fig.add_trace(
        go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line=dict(color='purple'), name='CCI', yaxis='y3'))
    fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False, yaxis='y4'))

    return fig


def origin_data(ticker_data, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close', yaxis='y1'))
    fig = common_traces(ticker_data, ticker, fig)
    fig.update_layout(
        plot_bgcolor='rgba(240, 240, 240, 0.5)',
        paper_bgcolor='rgba(240, 240, 240, 0.5)',
        height=900,
        title=f'Ticker: {ticker}',
        hovermode='x unified',
        yaxis1=dict(domain=[0.5, 1], anchor='x', title='Close', title_standoff=10),
        yaxis2=dict(domain=[0.30, 0.45], anchor='x', title='RSI', title_standoff=10),
        yaxis3=dict(domain=[0.10, 0.28], anchor='x', title='CCI', title_standoff=10),
        yaxis4=dict(domain=[0, 0.09], anchor='x', title='Volume', title_standoff=10),
        xaxis=dict(domain=[0, 1]),
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey', dtick='M3')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')

    return fig


def res_data(ticker_data, ticker, entry_points, exit_points):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=entry_points['Date'],
                             y=entry_points['Close'],
                             mode='markers',
                             marker=dict(color='green', size=9),
                             name='Entry'))

    fig.add_trace(go.Scatter(x=exit_points['Date'],
                             y=exit_points['Close'],
                             mode='markers',
                             marker=dict(color='red', size=9),
                             name='Exit'))

    fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', line=dict(color='#6495ED'),
                             name='Close', yaxis='y1'))
    fig = common_traces(ticker_data, ticker, fig)

    fig.update_layout(
        plot_bgcolor='rgba(240, 240, 240, 0.5)',
        paper_bgcolor='rgba(240, 240, 240, 0.5)',
        height=900,
        title=f'Ticker: {ticker}',
        hovermode='x unified',
        yaxis1=dict(domain=[0.5, 1], anchor='x', title='Close', title_standoff=10),
        yaxis2=dict(domain=[0.30, 0.45], anchor='x', title='RSI', title_standoff=10),
        yaxis3=dict(domain=[0.10, 0.28], anchor='x', title='CCI', title_standoff=10),
        yaxis4=dict(domain=[0, 0.09], anchor='x', title='Volume', title_standoff=10),
        xaxis=dict(domain=[0, 1]),
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey', dtick='M3')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')

    return fig




def stats_data(ticker):
    rows1 = generate_rows(ticker, strategy_summaries)
    stats_df1 = pd.DataFrame(rows1)

    rows2 = generate_rows(ticker, strategy_summaries2)
    stats_df2 = pd.DataFrame(rows2)

    stats_df1_vertical = stats_df1.set_index('Strategy').T
    stats_df2_vertical = stats_df2.set_index('Strategy').T
    stats_df1_vertical.columns = [col.replace(ticker + '_', '') for col in stats_df1_vertical.columns]
    stats_df2_vertical.columns = [col.replace(ticker + '_', '') for col in stats_df2_vertical.columns]
    # fig = go.Figure()
    fig = make_subplots(rows=2, cols=3, specs=[[{'type': 'table'}, {'type': 'xy'}, {'type': 'xy'}]]*2,)

    sharpe_colors = ['#A9A9A9', '#6495ED', '#E9967A']
    total_return_colors = ['#B8860B', '#FF8C00', 'lightblue']
    fig.add_annotation(
        xref="x domain", yref="y domain",
        x=0.5, y=1.1,
        text="Sharpe Ratio",
        showarrow=False,
        font=dict(size=16)
    )
    fig.add_annotation(
        xref="x2 domain", yref="y2 domain",
        x=0.5, y=1.1,
        text="Total Return (%)",
        showarrow=False,
        font=dict(size=16)
    )

    fig.add_trace(go.Bar(
        x=stats_df2_vertical.columns,
        y=stats_df2_vertical.loc['Sharpe'],
        name='Default sharpe',
        orientation='v',
        opacity=0.7,
        width=0.38,
        showlegend=True,
        legendrank=1,
        text=stats_df2_vertical.loc['Sharpe'],
        textposition='auto',
        texttemplate='%{text:.2f}',
        textfont=dict(size=16),
    ), row=1, col=2)


    fig.add_trace(go.Bar(
        x=stats_df1_vertical.columns,
        y=stats_df1_vertical.loc['Sharpe'],
        name='Optimized sharpe',
        orientation='v',
        marker=dict(color=sharpe_colors),
        width=0.38,
        opacity=0.7,
        text=stats_df1_vertical.loc['Sharpe'],
        textposition='auto',
        texttemplate='%{text:.2f}',
        textfont=dict(size=16),
    ), row=1, col=2)


    fig.add_trace(go.Table(
        header=dict(values=['Optimized parameters'] + stats_df1_vertical.columns[0:].tolist(),
                    fill_color='lightskyblue',
                    align='left',
                    font=dict(size=18, color='black')),
        cells=dict(values=[stats_df1_vertical.index] + [stats_df1_vertical[col] for col in stats_df1_vertical.columns],
                   fill_color='lightgray',
                   align='left',
                   font=dict(size=16, color='black'),
                   height=30),
        columnwidth=[0.4, 0.2, 0.2, 0.2],
    ), row=1, col=1)


    fig.add_trace(go.Bar(
        x=stats_df2_vertical.columns,
        y=stats_df2_vertical.loc['Sharpe'],
        name='Default sharpe',
        orientation='v',
        marker=dict(color=sharpe_colors),
        width=0.38,
        opacity=0.7,
        text=stats_df2_vertical.loc['Sharpe'],
        textposition='auto',
        texttemplate='%{text:.2f}',
        textfont=dict(size=16),

    ), row=2, col=2)

    fig.add_trace(go.Bar(
        x=stats_df2_vertical.columns,
        y=stats_df2_vertical.loc['Total return (%)'],
        name='Default ret',
        orientation='v',
        opacity=0.7,
        width=0.38,
        text=stats_df2_vertical.loc['Total return (%)'],
        textposition='auto',
        texttemplate='%{text:.2f}',
        textfont=dict(size=16),
    ), row=1, col=3)

    fig.add_trace(go.Bar(
        x=stats_df1_vertical.columns,
        y=stats_df1_vertical.loc['Total return (%)'],
        name='Optimized ret',
        orientation='v',
        marker=dict(color=total_return_colors),
        width=0.38,
        opacity=0.7,
        text=stats_df1_vertical.loc['Total return (%)'],
        textposition='auto',
        texttemplate='%{text:.2f}',
        textfont=dict(size=16),
    ), row=1, col=3)



    fig.add_trace(go.Bar(
        x=stats_df2_vertical.columns,
        y=stats_df2_vertical.loc['Total return (%)'],
        name='Default ret',
        orientation='v',
        marker=dict(color=total_return_colors),
        width=0.38,
        opacity=0.7,
        text=stats_df2_vertical.loc['Total return (%)'],
        textposition='auto',
        texttemplate='%{text:.2f}',
        textfont=dict(size=16),
    ), row=2, col=3)

    fig.update_xaxes(tickfont=dict(size=16), row=1, col=2)
    fig.update_xaxes(tickfont=dict(size=16), row=1, col=3)
    fig.update_xaxes(tickfont=dict(size=16), row=2, col=2)
    fig.update_xaxes(tickfont=dict(size=16), row=2, col=3)

    fig.add_trace(go.Table(
        header=dict(values=['Default  parameters'] + stats_df2_vertical.columns[0:].tolist(),
                    fill_color='#FFA07A',
                    align='left',
                    font=dict(size=18, color='black')),
        cells=dict(values=[stats_df2_vertical.index] + [stats_df2_vertical[col] for col in stats_df2_vertical.columns],
                   fill_color='lightgray',
                   align='left',
                   font=dict(size=16, color='black'),
                   height=40),
        columnwidth=[0.4, 0.2, 0.2, 0.2],
    ), row=2, col=1)


    return fig


def create_fig(data_type, ticker, start_date=None, end_date=None, selected_strategy="BB_RSI"):
    if data_type == 'Original Data':
        ticker_data = df[df['Ticker'] == ticker]
        fig = origin_data(ticker_data, ticker)
    elif data_type == 'Results Data':
        ticker_data = results_df[(results_df['Ticker'] == ticker) & (results_df['Strategy'] == selected_strategy)]
        entry_points = ticker_data[
            ((ticker_data['Actions'] == "OrderType.OPEN_LONG") | (ticker_data['Actions'] == "OrderType.OPEN_SHORT"))]
        exit_points = ticker_data[(ticker_data['Actions'] == '0')]
        fig = res_data(ticker_data, ticker, entry_points, exit_points)
    elif data_type == 'Stats':
        fig = stats_data(ticker)
    else:
        raise ValueError(f"Invalid data_type: {data_type}")

    return fig


@app.callback(
    Output("stock-graph", "figure"),
    [Input("data-type-dropdown", "value"),
     Input("ticker-dropdown", "value"),
     Input("strategy-selection", "value"),
     Input("apply-date-range", "n_clicks")],
    [State('start-date', 'value'),
     State('end-date', 'value')]
)
def update_graph(data_type, ticker, selected_strategy, n_clicks, start_date, end_date):
    return create_fig(data_type, ticker, start_date, end_date, selected_strategy)


@app.callback(
    Output('strategy-selection', 'style'),
    [Input('data-type-dropdown', 'value')]
)
def update_strategy_dropdown_visibility(data_type):
    if data_type == 'Results Data':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


def generate_rows(ticker, strategy_summaries):
    ticker_strategy_keys = [key for key in strategy_summaries.keys() if key.startswith(ticker)]
    strategy_results = {key: strategy_summaries[key] for key in ticker_strategy_keys}
    rows = []
    for strategy_name, summary in strategy_results.items():
        if not summary:  # Skip if the summary is empty
            continue

        row = {
            'Strategy': strategy_name,
            'Total return (%)': summary['Total return'],
            'Sharpe': summary['Sharpe'],
            # 'Sortino': summary['Sortino'],
            # 'Max balance drawdown': summary['Max balance drawdown'],
            'Max drawdown (%)': summary['Max drawdown'],
            'Returns std': summary['Returns std'],
            'Downside deviation': summary['Downside deviation'],
            'Best trade (%)': summary['Best trade'],
            'Worst trade (%)': summary['Worst trade'],
            'Positive trades (%)': summary['Positive trades'],
            'Positive trading days': summary['Positive trading days'],
        }
        rows.append(row)

    return rows


def update_stats(data_type, ticker):
    if data_type == 'Stats':
        return create_fig(data_type, ticker)
    else:
        return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)

# import cProfile
# if __name__ == '__main__':
#     cProfile.run('app.run_server(debug=True)', 'output_file.prof')
