from io import StringIO
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import json
import boto3


def find_sma_column(ticker_data):
    global sma_column
    for col_name in ticker_data.columns:
        if col_name.startswith('SMA_'):
            sma_column = col_name
            break
    return sma_column



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



def optional_indicators(ticker_data, ticker, fig, selected_indicators):
    if 'RSI' in selected_indicators:
        fig.add_trace(
            go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line=dict(color='blue'), name='RSI', yaxis='y2'))
    if 'CCI' in selected_indicators:
        fig.add_trace(
            go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line=dict(color='purple'), name='CCI', yaxis='y3'))
    if 'Volume' in selected_indicators:
        fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False, yaxis='y4'))