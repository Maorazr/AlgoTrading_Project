import dash
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

df = pd.read_csv('full_data', parse_dates=['Date'])  # replace with your actual data file
app = Dash(__name__)
server = app.server


app.layout = html.Div([
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
        value=df['Ticker'].unique()[0]
    ),
    dcc.Graph(id='stock-graph', config={
        'modeBarButtonsToAdd': [
            'drawline',
            'drawopenpath',
            'drawclosedpath',
            'drawcircle',
            'drawrect',
            'eraseshape'
        ]
    }),
    html.Div([
        html.Label("Start Date:"),
        dcc.Input(id='start-date', type='text', placeholder='YYYY-MM-DD'),
        html.Label("End Date:"),
        dcc.Input(id='end-date', type='text', placeholder='YYYY-MM-DD'),
        html.Button('Apply Date Range', id='apply-date-range', n_clicks=0),
    ]),
])

def create_fig(ticker, start_date=None, end_date=None):
    ticker_data = df[df['Ticker'] == ticker]

    # Filter the data based on the provided start and end dates
    if start_date and end_date:
        ticker_data = ticker_data[(ticker_data['Date'] >= pd.to_datetime(start_date)) & (ticker_data['Date'] <= pd.to_datetime(end_date))]

    fig = go.Figure()

    
    # fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close', yaxis='y1'))
    # fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BU'], line_color='green', name='BU', yaxis='y1'))
    # fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BL'], line_color='red', name='BL', yaxis='y1'))
    # fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['SMA_20'], line_color='orange', name='SMA_20', yaxis='y1'))
    # fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI', yaxis='y2'))
    # fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI', yaxis='y3'))
    # fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False, yaxis='y4'))

    # fig.update_layout(
    #     height=900,
    #     title=f'Ticker: {ticker}',
    #     hovermode='x unified',
    #     yaxis1=dict(domain=[0.6, 1], anchor='x', title='Close', title_standoff=10),
    #     yaxis2=dict(domain=[0.45, 0.6], anchor='x', title='Volume', title_standoff=10),
    #     yaxis3=dict(domain=[0.3, 0.45], anchor='x', title='RSI', title_standoff=10),
    #     yaxis4=dict(domain=[0, 0.3], anchor='x', title='CCI', title_standoff=10),
    #     xaxis=dict(domain=[0, 1]),
    # )
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



    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)
   
  

    return fig

@app.callback(
    Output("stock-graph", "figure"),
    [Input("ticker-dropdown", "value"),
     Input("apply-date-range", "n_clicks")],
    [State('start-date', 'value'),
     State('end-date', 'value')]
)
def update_graph(ticker, n_clicks, start_date, end_date):
    return create_fig(ticker, start_date, end_date)

if __name__ == '__main__':
    app.run_server(debug=True)
