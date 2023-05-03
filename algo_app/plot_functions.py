import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_interactive(df, ticker):
    ticker_data = df[df['Ticker'] == ticker]

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=(ticker, 'Volume', 'RSI', 'CCI'), vertical_spacing=0.1, row_heights=[0.4, 0.15, 0.15, 0.3])

    fig.add_trace(go.Candlestick(x=ticker_data['Date'],
                                 open=ticker_data['Open'],
                                 high=ticker_data['High'],
                                 low=ticker_data['Low'],
                                 close=ticker_data['Close'], showlegend=False,
                                 name='Candlestick'),
                  row=1, col=1)

    fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI'),
                  row=3, col=1)

    fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI'),
                  row=4, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)

    return fig
