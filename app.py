

import dash
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import json

df = pd.read_csv('sample_etf_data.csv', parse_dates=['Date'])  # replace with your actual data file
results_df = pd.read_csv('combined_results.csv', parse_dates=['Date'])

app = Dash(__name__)
server = app.server

with open('summary_results.json', 'r') as f:
    strategy_summaries = json.load(f)

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
    dcc.Graph(id='stock-graph'),
    html.Div([
        html.Label("Start Date:"),
        dcc.Input(id='start-date', type='text', placeholder='YYYY-MM-DD'),
        html.Label("End Date:"),
        dcc.Input(id='end-date', type='text', placeholder='YYYY-MM-DD'),
        html.Button('Apply Date Range', id='apply-date-range', n_clicks=0),
    ]),
    html.Div(id='stats-container', children=[dcc.Graph(id='stats')])

])

def create_fig(ticker, data_type, strategy_summaries, start_date=None, end_date=None):
    if data_type == 'Original Data':
        ticker_data = df[df['Ticker'] == ticker]
    elif data_type == 'Results Data':
        ticker_data = results_df[results_df['Ticker'] == ticker]
    elif data_type == 'Stats':
        ticker_strategy_keys = [key for key in strategy_summaries.keys() if key.startswith(ticker)]
        strategy_results = {key: strategy_summaries[key] for key in ticker_strategy_keys}
        rows = []
        for strategy_name, summary in strategy_results.items():
            row = {
                'Strategy': strategy_name,
                'Total return': summary['Total return'],
                'Sharpe': summary['Sharpe'],
                'Sortino': summary['Sortino'],
                'Max balance drawdown': summary['Max balance drawdown'],
                'Max drawdown': summary['Max drawdown'],
                'Returns std': summary['Returns std'],
                'Downside deviation': summary['Downside deviation'],
                'Best trade': summary['Best trade'],
                'Worst trade': summary['Worst trade'],
                'Positive trades': summary['Positive trades'],
                'Positive trading days': summary['Positive trading days'],
            }
            rows.append(row)

        stats_df = pd.DataFrame(rows)
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(stats_df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[stats_df[col] for col in stats_df.columns],
                    fill_color='lavender',
                    align='left'))
        ])

    else:
        raise ValueError(f"Invalid data_type: {data_type}")

    if start_date and end_date:
        ticker_data = ticker_data[(ticker_data['Date'] >= pd.to_datetime(start_date)) & (ticker_data['Date'] <= pd.to_datetime(end_date))]

    if data_type == 'Original Data':
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close', yaxis='y1'))
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BU'], line_color='green', name='BU', yaxis='y1'))
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BL'], line_color='red', name='BL', yaxis='y1'))
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['SMA_20'], line_color='orange', name='SMA_20', yaxis='y1'))
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI', yaxis='y2'))
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI', yaxis='y3'))
        fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False, yaxis='y4'))
        
        fig.update_layout(
            height=900,
            title=f'Ticker: {ticker}',
            hovermode='x unified',
            yaxis1=dict(domain=[0.5, 1], anchor='x', title='Close', title_standoff=10),
            yaxis2=dict(domain=[0.30, 0.5], anchor='x', title='RSI', title_standoff=10),
            yaxis3=dict(domain=[0.10, 0.30], anchor='x', title='CCI', title_standoff=10),
            yaxis4=dict(domain=[0, 0.10], anchor='x', title='Volume', title_standoff=10),
            xaxis=dict(domain=[0, 1]),
        )
    elif data_type == 'Results Data':
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['Open'], mode='lines', name='Portfolio size over time'))
        fig.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['Pos'], mode='lines', name='Pos'))
        fig.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['Balance'], mode='lines', name='Balance over time'))
        fig.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['Return rate with comm'], mode='lines', name='ret over time'))
        fig.update_layout(
            height=900,
            title=f'Ticker: {ticker}',
            hovermode='x unified',
            yaxis1=dict(domain=[0.5, 1], anchor='x', title='Close', title_standoff=10),
        )
    

    return fig

@app.callback(
    Output("stock-graph", "figure"),
    [Input("data-type-dropdown", "value"),
     Input("ticker-dropdown", "value"),
     Input("apply-date-range", "n_clicks")],
    [State('start-date', 'value'),
     State('end-date', 'value')]
)
def update_graph(data_type, ticker, n_clicks, start_date, end_date):
    return create_fig(ticker, data_type, strategy_summaries, start_date, end_date)


@app.callback(
    Output("stats", "figure"),
    [Input("data-type-dropdown", "value"),
     Input("ticker-dropdown", "value")]
)
def update_stats(data_type, ticker):
    if data_type == 'Stats':
        return create_fig(ticker, data_type, strategy_summaries)
    else:
        return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)

       
