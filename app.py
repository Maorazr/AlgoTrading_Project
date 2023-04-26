# # # # # # # # # import pandas as pd
# # # # # # # # # import dash
# # # # # # # # # import dash_core_components as dcc
# # # # # # # # # import dash_html_components as html
# # # # # # # # # from dash.dependencies import Input, Output
# # # # # # # # # from plot_functions import plot_interactive

# # # # # # # # # # Load your data and preprocess it here
# # # # # # # # # df = pd.read_csv('full_data', index_col=False)

# # # # # # # # # # Create the figure using the plot_interactive function
# # # # # # # # # fig = plot_interactive(df, 'AAPL')

# # # # # # # # # app = dash.Dash(__name__)

# # # # # # # # # app.layout = html.Div([
# # # # # # # # #     dcc.Graph(id='graph', figure=fig),
# # # # # # # # #     html.Div(id='hover-line-container')
# # # # # # # # # ])

# # # # # # # # # def create_hover_line(fig, hoverData):
# # # # # # # # #     if hoverData is None:
# # # # # # # # #         return fig

# # # # # # # # #     x_value = hoverData['points'][0]['x']
# # # # # # # # #     hover_line = {
# # # # # # # # #         'type': 'line',
# # # # # # # # #         'x0': x_value,
# # # # # # # # #         'x1': x_value,
# # # # # # # # #         'y0': 0,
# # # # # # # # #         'y1': 1,
# # # # # # # # #         'yref': 'paper',
# # # # # # # # #         'line': {
# # # # # # # # #             'color': 'black',
# # # # # # # # #             'width': 1
# # # # # # # # #         }
# # # # # # # # #     }

# # # # # # # # #     fig.update_layout(shapes=[hover_line])
# # # # # # # # #     return fig

# # # # # # # # # @app.callback(
# # # # # # # # #     Output('graph', 'figure'),
# # # # # # # # #     Input('graph', 'hoverData')
# # # # # # # # # )
# # # # # # # # # def update_hover_line(hoverData):
# # # # # # # # #     return create_hover_line(fig, hoverData)

# # # # # # # # # if __name__ == '__main__':
# # # # # # # # #     app.run_server(debug=True)



# # # # # # # # import dash
# # # # # # # # import dash_core_components as dcc
# # # # # # # # import dash_html_components as html
# # # # # # # # from dash.dependencies import Input, Output
# # # # # # # # import plotly.graph_objects as go
# # # # # # # # import pandas as pd
# # # # # # # # from plotly.subplots import make_subplots
# # # # # # # # df = pd.read_csv('full_data')  # replace with your actual data file

# # # # # # # # app = dash.Dash(__name__)

# # # # # # # # app.layout = html.Div([
# # # # # # # #     dcc.Dropdown(
# # # # # # # #         id='ticker-dropdown',
# # # # # # # #         options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
# # # # # # # #         value=df['Ticker'].unique()[0]
# # # # # # # #     ),
# # # # # # # #     dcc.Graph(id='stock-graph'),
# # # # # # # # ])

# # # # # # # # def create_hover_line(fig):
# # # # # # # #     fig.update_layout(
# # # # # # # #         hovermode="x unified",
# # # # # # # #         updatemenus=[
# # # # # # # #             dict(
# # # # # # # #                 type="buttons",
# # # # # # # #                 showactive=False,
# # # # # # # #                 buttons=list(
# # # # # # # #                     [
# # # # # # # #                         dict(
# # # # # # # #                             label="Enable Hover",
# # # # # # # #                             method="update",
# # # # # # # #                             args=[
# # # # # # # #                                 {"visible": [True, True, True, True]},
# # # # # # # #                                 {"title": "Hover enabled"},
# # # # # # # #                             ],
# # # # # # # #                         ),
# # # # # # # #                         dict(
# # # # # # # #                             label="Disable Hover",
# # # # # # # #                             method="update",
# # # # # # # #                             args=[
# # # # # # # #                                 {"visible": [False, False, False, False]},
# # # # # # # #                                 {"title": "Hover disabled"},
# # # # # # # #                             ],
# # # # # # # #                         ),
# # # # # # # #                     ]
# # # # # # # #                 ),
# # # # # # # #             )
# # # # # # # #         ],
# # # # # # # #     )
# # # # # # # #     return fig

# # # # # # # # @app.callback(
# # # # # # # #     Output('stock-graph', 'figure'),
# # # # # # # #     [Input('ticker-dropdown', 'value')]
# # # # # # # # )
# # # # # # # # # def update_graph(ticker):
# # # # # # # # #     ticker_data = df[df['Ticker'] == ticker]
    
# # # # # # # # #     fig = go.Figure()
# # # # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close'))
# # # # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BU'], mode='lines', name='Upper Band', line=dict(color='rgba(0, 100, 80, 0.5)')))
# # # # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BL'], mode='lines', name='Lower Band', line=dict(color='rgba(230, 0, 0, 0.5)')))
# # # # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['SMA_20'], mode='lines', name='SMA_20', line=dict(color='rgba(0, 0, 200, 0.5)')))

# # # # # # # # #     fig.update_layout(title=f"Stock Data for {ticker}", xaxis_title="Date", yaxis_title="Price")
# # # # # # # # #     fig = create_hover_line(fig)
    
# # # # # # # # #     return fig
# # # # # # # # def update_graph(ticker):
# # # # # # # #     ticker_data = df[df['Ticker'] == ticker]
    
# # # # # # # #     # fig = go.Figure()
# # # # # # # #     fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=(ticker, 'Volume', 'RSI', 'CCI'), vertical_spacing=0.05, row_heights=[0.4, 0.15, 0.15, 0.3])
# # # # # # # #     # fig.add_trace(go.Candlestick(x=ticker_data['Date'],
# # # # # # # #     #                              open=ticker_data['Open'],
# # # # # # # #     #                              high=ticker_data['High'],
# # # # # # # #     #                              low=ticker_data['Low'],
# # # # # # # #     #                              close=ticker_data['Close'], showlegend=False,
# # # # # # # #     #                              name='Candlestick'))
# # # # # # # #     # fig = go.Figure()
# # # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'],
# # # # # # # #                              y=ticker_data['SMA_20'],
# # # # # # # #                              line_color='black',
# # # # # # # #                              name='SMA_20'),
# # # # # # # #                   row=1, col=1)

# # # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'],
# # # # # # # #                              y=ticker_data['BU'],
# # # # # # # #                              line_color='gray',
# # # # # # # #                              line={'dash': 'dash'},
# # # # # # # #                              name='Upper Band',
# # # # # # # #                              opacity=0.5),
# # # # # # # #                   row=1, col=1)

# # # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'],
# # # # # # # #                              y=ticker_data['BL'],
# # # # # # # #                              line_color='gray',
# # # # # # # #                              line={'dash': 'dash'},
# # # # # # # #                              fill='tonexty',
# # # # # # # #                              name='Lower Band',
# # # # # # # #                              opacity=0.5),
# # # # # # # #                   row=1, col=1)
        
# # # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close'))

# # # # # # # #     fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False),
# # # # # # # #                   row=2, col=1)

# # # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI'),
# # # # # # # #                   row=3, col=1)

# # # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI'),
# # # # # # # #                   row=4, col=1)
# # # # # # # #     # fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BU'], mode='lines', name='Upper Band', line=dict(color='rgba(0, 100, 80, 0.5)')))
# # # # # # # #     # fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BL'], mode='lines', name='Lower Band', line=dict(color='rgba(230, 0, 0, 0.5)')))
# # # # # # # #     # fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['SMA_20'], mode='lines', name='SMA_20', line=dict(color='rgba(0, 0, 200, 0.5)')))

# # # # # # # #     # fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Volume'], line_color='blue', name='Volume'))

# # # # # # # #     # fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='purple', name='RSI'))

# # # # # # # #     # fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='orange', name='CCI'))

# # # # # # # #     # Update the layout
# # # # # # # #     fig.update_layout(height=800, title=f'Ticker: {ticker}', hovermode='x unified')
# # # # # # # #     fig.update_xaxes(showspikes=True)
# # # # # # # #     fig.update_yaxes(showspikes=True)
    
# # # # # # # #     create_hover_line(fig)
# # # # # # # #     return fig

# # # # # # # # if __name__ == '__main__':
# # # # # # # #     app.run_server(debug=True)
# # # # # # # import dash
# # # # # # # import dash_core_components as dcc
# # # # # # # import dash_html_components as html
# # # # # # # from dash.dependencies import Input, Output
# # # # # # # import plotly.graph_objects as go
# # # # # # # import pandas as pd
# # # # # # # from plotly.subplots import make_subplots

# # # # # # # df = pd.read_csv('full_data')  # replace with your actual data file

# # # # # # # app = dash.Dash(__name__)

# # # # # # # app.layout = html.Div([
# # # # # # #     dcc.Dropdown(
# # # # # # #         id='ticker-dropdown',
# # # # # # #         options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
# # # # # # #         value=df['Ticker'].unique()[0]
# # # # # # #     ),
# # # # # # #     dcc.Graph(id='stock-graph'),
# # # # # # # ])

# # # # # # # @app.callback(
# # # # # # #     Output('stock-graph', 'figure'),
# # # # # # #     [Input('ticker-dropdown', 'value')]
# # # # # # # )
# # # # # # # def update_graph(ticker):
# # # # # # #     ticker_data = df[df['Ticker'] == ticker]
    
# # # # # # #     fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=(ticker, 'Volume', 'RSI', 'CCI'), vertical_spacing=0.05, row_heights=[0.4, 0.15, 0.15, 0.3])

# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close'), row=1, col=1)

# # # # # # #     fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False), row=2, col=1)

# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI'), row=3, col=1)

# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI'), row=4, col=1)

# # # # # # #     fig.update_layout(height=800, title=f'Ticker: {ticker}', hovermode='x unified')
# # # # # # #     fig.update_xaxes(showspikes=True)
# # # # # # #     fig.update_yaxes(showspikes=True)

# # # # # # #     return fig

# # # # # # # if __name__ == '__main__':
# # # # # # #     app.run_server(debug=True)
# # # # # # # import dash
# # # # # # # import dash_core_components as dcc
# # # # # # # import dash_html_components as html
# # # # # # # from dash.dependencies import Input, Output
# # # # # # # import plotly.graph_objects as go
# # # # # # # import pandas as pd
# # # # # # # from plotly.subplots import make_subplots

# # # # # # # df = pd.read_csv('full_data')  # replace with your actual data file

# # # # # # # app = dash.Dash(__name__)

# # # # # # # app.layout = html.Div([
# # # # # # #     dcc.Dropdown(
# # # # # # #         id='ticker-dropdown',
# # # # # # #         options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
# # # # # # #         value=df['Ticker'].unique()[0]
# # # # # # #     ),
# # # # # # #     dcc.Graph(id='stock-graph'),
# # # # # # # ])

# # # # # # # @app.callback(
# # # # # # #     Output('stock-graph', 'figure'),
# # # # # # #     [Input('ticker-dropdown', 'value')]
# # # # # # # )
# # # # # # # def update_graph(ticker):
# # # # # # #     ticker_data = df[df['Ticker'] == ticker]
    
# # # # # # #     fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=(ticker, 'Volume', 'RSI', 'CCI'), vertical_spacing=0.05, row_heights=[0.4, 0.15, 0.15, 0.3])

# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close'), row=1, col=1)

# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BU'], mode='lines', name='Upper Band', line=dict(color='rgba(0, 100, 80, 0.5)')), row=1, col=1)
# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BL'], mode='lines', name='Lower Band', line=dict(color='rgba(230, 0, 0, 0.5)')), row=1, col=1)
# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['SMA_20'], mode='lines', name='SMA_20', line=dict(color='rgba(0, 0, 200, 0.5)')), row=1, col=1)

# # # # # # #     fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False), row=2, col=1)

# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI'), row=3, col=1)

# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI'), row=4, col=1)

# # # # # # #     fig.update_layout(height=800, title=f'Ticker: {ticker}', hovermode='x unified')
# # # # # # #     fig.update_xaxes(showspikes=True)
# # # # # # #     fig.update_yaxes(showspikes=True)

# # # # # # #     return fig




# # # # # # # import dash
# # # # # # # from dash import dcc
# # # # # # # from dash import html
# # # # # # # from dash.dependencies import Input, Output
# # # # # # # import plotly.graph_objects as go
# # # # # # # import pandas as pd
# # # # # # # from plotly.subplots import make_subplots

# # # # # # # df = pd.read_csv('full_data')  # replace with your actual data file

# # # # # # # app = dash.Dash(__name__)

# # # # # # # app.layout = html.Div([
# # # # # # #     dcc.Dropdown(
# # # # # # #         id='ticker-dropdown',
# # # # # # #         options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
# # # # # # #         value=df['Ticker'].unique()[0]
# # # # # # #     ),
# # # # # # #     dcc.Graph(id='stock-graph'),
# # # # # # # ])

# # # # # # # def create_fig(ticker_data, selected_ticker):
# # # # # # #     fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=(selected_ticker, 'Volume', 'RSI', 'CCI'), vertical_spacing=0.05, row_heights=[0.4, 0.15, 0.15, 0.3])

# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close'), row=1, col=1)

# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BU'], mode='lines', name='Upper Band', line=dict(color='rgba(0, 100, 80, 0.5)')), row=1, col=1)
# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BL'], mode='lines', name='Lower Band', line=dict(color='rgba(230, 0, 0, 0.5)')), row=1, col=1)
# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['SMA_20'], mode='lines', name='SMA_20', line=dict(color='rgba(0, 0, 200, 0.5)')), row=1, col=1)

# # # # # # #     fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False), row=2, col=1)

# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI'), row=3, col=1)

# # # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI'), row=4, col=1)

# # # # # # #     fig.update_layout(height=800, title=f'Ticker: {selected_ticker}', hovermode='x unified')
# # # # # # #     fig.update_xaxes(showspikes=True, spikemode='across', spikesnap='cursor', spikedash='solid', spikethickness=1)
# # # # # # #     fig.update_yaxes(showspikes=True, spikemode='across', spikesnap='cursor', spikedash='solid', spikethickness=1)
# # # # # # #     # fig.update_xaxes(showspikes=True)
# # # # # # #     # fig.update_yaxes(showspikes=True)

# # # # # # #     return fig

# # # # # # # @app.callback(
# # # # # # #     Output('stock-graph', 'figure'),
# # # # # # #     [Input('ticker-dropdown', 'value')]
# # # # # # # )
# # # # # # # def update_graph(selected_ticker):
# # # # # # #     ticker_data = df[df['Ticker'] == selected_ticker]
# # # # # # #     fig = create_fig(ticker_data, selected_ticker)
# # # # # # #     return fig


# # # # # # # # @app.callback(
# # # # # # # #     Output('stock-graph', 'extendData'),
# # # # # # # #     [Input('stock-graph', 'hoverData')],
# # # # # # # #     [dash.dependencies.State('stock-graph', 'figure')]
# # # # # # # # )
# # # # # # # # def display_hover_line(hoverData, figure):
# # # # # # # #     if hoverData is None:
# # # # # # # #         return None

# # # # # # # #     x_value = hoverData['points'][0]['x']

# # # # # # # #     shapes = [
# # # # # # # #         {
# # # # # # # #             'type': 'line',
# # # # # # # #             'x0': x_value,
# # # # # # # #             'x1': x_value,
# # # # # # # #             'y0': 0,
# # # # # # # #             'y1': 1,
# # # # # # # #             'yref': f'y{row}' if row > 1 else 'y',
# # # # # # # #             'xref': f'x{row}' if row > 1 else 'x',
# # # # # # # #             'line': {
# # # # # # # #                 'color': 'black',
# # # # # # # #                 'width': 1
# # # # # # # #             }
# # # # # # # #         }
# # # # # # # #         for row in range(1, 5)
# # # # # # # #     ]

# # # # # # #     # return {'layout': {'shapes': shapes}}


# # # # # # # if __name__ == '__main__':
# # # # # # #     app.run_server(debug=True)


# # # # # # import pandas as pd
# # # # # # from dash import dcc
# # # # # # from dash import html
# # # # # # from dash import Dash
# # # # # # from dash.dependencies import Input, Output
# # # # # # from plotly.subplots import make_subplots
# # # # # # import plotly.graph_objs as go

# # # # # # # Replace this with your actual data file
# # # # # # df = pd.read_csv('full_data')

# # # # # # app = Dash(__name__)

# # # # # # app.layout = html.Div([
# # # # # #     dcc.Dropdown(
# # # # # #         id='ticker-dropdown',
# # # # # #         options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
# # # # # #         value=df['Ticker'].unique()[0]
# # # # # #     ),
# # # # # #     dcc.Graph(id='stock-graph'),
# # # # # # ])

# # # # # # def create_fig(ticker_data, selected_ticker):
# # # # # #     fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=(selected_ticker, 'Volume', 'RSI', 'CCI'), vertical_spacing=0.05, row_heights=[0.4, 0.15, 0.15, 0.3])

# # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close'), row=1, col=1)

# # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BU'], mode='lines', name='Upper Band', line=dict(color='rgba(0, 100, 80, 0.5)')), row=1, col=1)
# # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BL'], mode='lines', name='Lower Band', line=dict(color='rgba(230, 0, 0, 0.5)')), row=1, col=1)
# # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['SMA_20'], mode='lines', name='SMA_20', line=dict(color='rgba(0, 0, 200, 0.5)')), row=1, col=1)

# # # # # #     fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False), row=2, col=1)

# # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI'), row=3, col=1)

# # # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI'), row=4, col=1)

# # # # # #     fig.update_layout(height=800, title=f'Ticker: {selected_ticker}', hovermode='x unified')

# # # # # #     # Configure spike lines
# # # # # #     fig.update_xaxes(showspikes=True, spikemode='across', spikesnap='cursor', spikedash='solid', spikethickness=1)
# # # # # #     fig.update_yaxes(showspikes=True, spikemode='across', spikesnap='cursor', spikedash='solid', spikethickness=1)

# # # # # #     fig.update_layout(
# # # # # #     updatemenus=[
# # # # # #         dict(
# # # # # #             type="buttons",
# # # # # #             showactive=False,
# # # # # #             buttons=list([
# # # # # #                 dict(
# # # # # #                     label="Enable Hover",
# # # # # #                     method="relayout",
# # # # # #                     args=["spikemode", "across"]
# # # # # #                 ),
# # # # # #                 dict(
# # # # # #                     label="Disable Hover",
# # # # # #                     method="relayout",
# # # # # #                     args=["spikemode", "none"]
# # # # # #                 )
# # # # # #             ]),
# # # # # #             direction="left",
# # # # # #             pad={"r": 10, "t": 10},
# # # # # #             x=0.4,
# # # # # #             xanchor="left",
# # # # # #             y=1.12,
# # # # # #             yanchor="top"
# # # # # #         ),
# # # # # #     ]
# # # # # # )
# # # # # #     return fig

# # # # # # @app.callback(
# # # # # #     Output('stock-graph', 'figure'),
# # # # # #     [Input('ticker-dropdown', 'value')]
# # # # # # )
# # # # # # def update_graph(selected_ticker):
# # # # # #     ticker_data = df[df['Ticker'] == selected_ticker]
# # # # # #     fig = create_fig(ticker_data, selected_ticker)
# # # # # #     return fig

# # # # # # if __name__ == '__main__':
# # # # # #     app.run_server(debug=True)


# # # # # import pandas as pd
# # # # # import plotly.graph_objects as go
# # # # # from plotly.subplots import make_subplots
# # # # # from dash import Dash, dcc, html
# # # # # from dash.dependencies import Input, Output, State

# # # # # df = pd.read_csv('full_data')  # replace with your actual data file

# # # # # app = Dash(__name__)

# # # # # app.layout = html.Div([
# # # # #     dcc.Dropdown(
# # # # #         id='ticker-dropdown',
# # # # #         options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
# # # # #         value=df['Ticker'].unique()[0]
# # # # #     ),
# # # # #     dcc.Graph(id='stock-graph'),
# # # # # ])


# # # # # def create_fig(ticker):
# # # # #     ticker_data = df[df['Ticker'] == ticker]
# # # # #     fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=(ticker, 'Volume', 'RSI', 'CCI'), vertical_spacing=0.05, row_heights=[0.4, 0.15, 0.15, 0.3])

# # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close'), row=1, col=1)
# # # # #     fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False), row=2, col=1)
# # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI'), row=3, col=1)
# # # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI'), row=4, col=1)

# # # # #     fig.update_layout(height=800, title=f'Ticker: {ticker}', hovermode='x unified')
# # # # #     fig.update_xaxes(showspikes=True)
# # # # #     fig.update_yaxes(showspikes=True)

# # # # #     return fig


# # # # # # @app.callback(
# # # # # #     Output("stock-graph", "figure"),
# # # # # #     Input("ticker-dropdown", "value"),
# # # # # #     State("stock-graph", "figure"),
# # # # # # )
# # # # # def update_graph(ticker, figure):
# # # # #     return create_fig(ticker)


# # # # # @app.callback(
# # # # #     Output("stock-graph", "figure"),
# # # # #     Input("stock-graph", "hoverData"),
# # # # #     State("stock-graph", "figure"),
# # # # #     State("ticker-dropdown", "value"),
# # # # # )
# # # # # def update_hover_line(hoverData, figure, ticker):
# # # # #     if hoverData is None:
# # # # #         return create_fig(ticker)

# # # # #     fig = go.Figure(figure)
# # # # #     x_value = hoverData["points"][0]["x"]

# # # # #     # Clear existing shapes
# # # # #     fig.update_layout(shapes=[])

# # # # #     # Add vertical line to each subplot
# # # # #     for row in range(1, 5):
# # # # #         hover_line = {
# # # # #             "type": "line",
# # # # #             "x0": x_value,
# # # # #             "x1": x_value,
# # # # #             "y0": 0,
# # # # #             "y1": 1,
# # # # #             "yref": f"y{row}" if row > 1 else "y",
# # # # #             "xref": "x",
# # # # #             "line": {"color": "black", "width": 1},
# # # # #         }
# # # # #         fig.add_shape(hover_line)

# # # # #     # Update hover text
# # # # #     fig.update_traces(hovertemplate=f"<b>Date</b>: {x_value}<br><b>Value</b>: %{{y}}")

# # # # #     return fig


# # # # # if __name__ == '__main__':
# # # # #     app.run_server(debug=True)



# # # # import pandas as pd
# # # # import plotly.graph_objects as go
# # # # from dash import Dash, dcc, html
# # # # from dash.dependencies import Input, Output

# # # # df = pd.read_csv('full_data')  # replace with your actual data file

# # # # app = Dash(__name__)

# # # # app.layout = html.Div([
# # # #     dcc.Dropdown(
# # # #         id='ticker-dropdown',
# # # #         options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
# # # #         value=df['Ticker'].unique()[0]
# # # #     ),
# # # #     dcc.Graph(id='stock-graph'),
# # # # ])


# # # # def create_fig(ticker):
# # # #     ticker_data = df[df['Ticker'] == ticker]

# # # #     fig = go.Figure()

# # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close', yaxis='y1'))
# # # #     fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False, yaxis='y2'))
# # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI', yaxis='y3'))
# # # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI', yaxis='y4'))

# # # #     fig.update_layout(
# # # #         height=800,
# # # #         title=f'Ticker: {ticker}',
# # # #         hovermode='x unified',
# # # #         yaxis1=dict(domain=[0.6, 1], anchor='x', title='Close'),
# # # #         yaxis2=dict(domain=[0.45, 0.6], anchor='x', title='Volume'),
# # # #         yaxis3=dict(domain=[0.3, 0.45], anchor='x', title='RSI'),
# # # #         yaxis4=dict(domain=[0, 0.3], anchor='x', title='CCI'),
# # # #         xaxis=dict(domain=[0, 1]),
# # # #     )

# # # #     fig.update_xaxes(showspikes=True)
# # # #     fig.update_yaxes(showspikes=True)

# # # #     return fig


# # # # @app.callback(
# # # #     Output("stock-graph", "figure"),
# # # #     Input("ticker-dropdown", "value"),
# # # # )
# # # # def update_graph(ticker):
# # # #     return create_fig(ticker)


# # # # if __name__ == '__main__':
# # # #     app.run_server(debug=True)

# # # import dash
# # # import pandas as pd
# # # import plotly.graph_objects as go
# # # from dash import Dash, dcc, html
# # # from dash.dependencies import Input, Output

# # # df = pd.read_csv('full_data')  # replace with your actual data file

# # # app = Dash(__name__)

# # # app.layout = html.Div([
# # #     dcc.Dropdown(
# # #         id='ticker-dropdown',
# # #         options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
# # #         value=df['Ticker'].unique()[0]
# # #     ),
# # #     dcc.Graph(id='stock-graph', config={
# # #         'modeBarButtonsToAdd': [
# # #             'drawline',
# # #             'drawopenpath',
# # #             'drawclosedpath',
# # #             'drawcircle',
# # #             'drawrect',
# # #             'eraseshape'
# # #         ]
# # #     }),
# # #     html.Div([
# # #         html.Label("Search Date:"),
# # #         dcc.Input(id='search-date', type='search'),
# # #         html.Button('Search', id='search-button', n_clicks=0),
# # #     ]),
# # # ])


# # # def create_fig(ticker, date_range ,search_date=None):
# # #     ticker_data = df[df['Ticker'] == ticker]


# # #     # Filter the data based on the selected date range
# # #     ticker_data = ticker_data[(ticker_data['Date'] >= pd.to_datetime(date_range[0], unit='s')) & (ticker_data['Date'] <= pd.to_datetime(date_range[1], unit='s'))]
# # #     fig = go.Figure()

# # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close', yaxis='y1'))
# # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BU'], line_color='green', name='BU', yaxis='y1'))
# # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BL'], line_color='red', name='BL', yaxis='y1'))
# # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['SMA_20'], line_color='orange', name='SMA_20', yaxis='y1'))
# # #     fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False, yaxis='y2'))
# # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI', yaxis='y3'))
# # #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI', yaxis='y4'))

# # #     fig.update_layout(
# # #         height=900,
# # #         title=f'Ticker: {ticker}',
# # #         hovermode='x unified',
# # #         yaxis1=dict(domain=[0.6, 1], anchor='x', title='Close'),
# # #         yaxis2=dict(domain=[0.45, 0.6], anchor='x', title='Volume'),
# # #         yaxis3=dict(domain=[0.3, 0.45], anchor='x', title='RSI'),
# # #         yaxis4=dict(domain=[0, 0.3], anchor='x', title='CCI'),
# # #         xaxis=dict(domain=[0, 1]),
# # #     )

    
# # #     fig.update_xaxes(showspikes=True)
# # #     fig.update_yaxes(showspikes=True)

# # #     if search_date:
# # #         fig.update_xaxes(range=[search_date, ticker_data['Date'].iloc[-1]])


# # #     return fig


# # # @app.callback(
# # #     Output("stock-graph", "figure"),
# # #     [Input("ticker-dropdown", "value"),
# # #      Input("search-button", "n_clicks")],
# # #     [dash.dependencies.State('search-date', 'value')]
# # # )
# # # def update_graph(ticker, date_range, search_date):
# # #     return create_fig(ticker, date_range, search_date)

# # # if __name__ == '__main__':
# # #     app.run_server(debug=True)


# # import pandas as pd
# # import plotly.graph_objects as go
# # from dash import Dash, dcc, html
# # from dash.dependencies import Input, Output, State

# # df = pd.read_csv('full_data')  # replace with your actual data file
# # df['Date'] = pd.to_datetime(df['Date'])

# # app = Dash(__name__)

# # app.layout = html.Div([
# #     dcc.Dropdown(
# #         id='ticker-dropdown',
# #         options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
# #         value=df['Ticker'].unique()[0]
# #     ),
# #     dcc.Graph(id='stock-graph', config={
# #         'modeBarButtonsToAdd': [
# #             'drawline',
# #             'drawopenpath',
# #             'drawclosedpath',
# #             'drawcircle',
# #             'drawrect',
# #             'eraseshape'
# #         ]
# #     }),
# #     html.Div([
# #         html.Label("Search Date:"),
# #         dcc.Input(id='search-date', type='date'),
# #         html.Button('Search', id='search-button', n_clicks=0),
# #     ]),
# # ])

# # def create_fig(ticker, search_date=None):
# #     ticker_data = df[df['Ticker'] == ticker]

# # # Filter the data based on the selected date range
# #     ticker_data = ticker_data[(ticker_data['Date'] >= pd.to_datetime(date_range[0], unit='s')) & (ticker_data['Date'] <= pd.to_datetime(date_range[1], unit='s'))]
# #     fig = go.Figure()

# #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close', yaxis='y1'))
# #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BU'], line_color='green', name='BU', yaxis='y1'))
# #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BL'], line_color='red', name='BL', yaxis='y1'))
# #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['SMA_20'], line_color='orange', name='SMA_20', yaxis='y1'))
# #     fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False, yaxis='y2'))
# #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI', yaxis='y3'))
# #     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI', yaxis='y4'))

# #     fig.update_layout(
# #         height=900,
# #         title=f'Ticker: {ticker}',
# #         hovermode='x unified',
# #         yaxis1=dict(domain=[0.6, 1], anchor='x', title='Close'),
# #         yaxis2=dict(domain=[0.45, 0.6], anchor='x', title='Volume'),
# #         yaxis3=dict(domain=[0.3, 0.45], anchor='x', title='RSI'),
# #         yaxis4=dict(domain=[0, 0.3], anchor='x', title='CCI'),
# #         xaxis=dict(domain=[0, 1]),
# #     )

    
# #     fig.update_xaxes(showspikes=True)
# #     fig.update_yaxes(showspikes=True)

# #     if search_date:
# #         search_date = pd.to_datetime(search_date)
# #         fig.update_xaxes(range=[search_date, ticker_data['Date'].iloc[-1]])

# #     return fig

# # @app.callback(
# #     Output("stock-graph", "figure"),
# #     [Input("ticker-dropdown", "value"),
# #      Input("search-button", "n_clicks")],
# #     [State('search-date', 'value')]
# # )
# # def update_graph(ticker, n_clicks, search_date):
# #     return create_fig(ticker, search_date)

# # if __name__ == '__main__':
# #     app.run_server(debug=True)


# import pandas as pd
# import plotly.graph_objects as go
# from dash import Dash, dcc, html
# from dash.dependencies import Input, Output, State

# df = pd.read_csv('full_data')  # replace with your actual data file
# df['Date'] = pd.to_datetime(df['Date'])

# app = Dash(__name__)

# app.layout = html.Div([
#     dcc.Dropdown(
#         id='ticker-dropdown',
#         options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
#         value=df['Ticker'].unique()[0]
#     ),
#     dcc.Graph(id='stock-graph', config={
#         'modeBarButtonsToAdd': [
#             'drawline',
#             'drawopenpath',
#             'drawclosedpath',
#             'drawcircle',
#             'drawrect',
#             'eraseshape'
#         ]
#     }),
#     html.Div([
#         html.Label("Search Date:"),
#         dcc.Input(id='search-date', type='text'),
#         html.Button('Search', id='search-button', n_clicks=0),
#     ]),
# ])

# def create_fig(ticker, search_date=None):
#     ticker_data = df[df['Ticker'] == ticker]

#     fig = go.Figure()

#     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close', yaxis='y1'))
#     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BU'], line_color='green', name='BU', yaxis='y1'))
#     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BL'], line_color='red', name='BL', yaxis='y1'))
#     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['SMA_20'], line_color='orange', name='SMA_20', yaxis='y1'))
#     fig.add_trace(go.Bar(x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False, yaxis='y2'))
#     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line_color='blue', name='RSI', yaxis='y3'))
#     fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line_color='purple', name='CCI', yaxis='y4'))

#     fig.update_layout(
#         height=900,
#         title=f'Ticker: {ticker}',
#         hovermode='x unified',
#         yaxis1=dict(domain=[0.6, 1], anchor='x', title='Close'),
#         yaxis2=dict(domain=[0.45, 0.6], anchor='x', title='Volume'),
#         yaxis3=dict(domain=[0.3, 0.45], anchor='x', title='RSI'),
#         yaxis4=dict(domain=[0, 0.3], anchor='x', title='CCI'),
#         xaxis=dict(domain=[0, 1]),
#     )

#     fig.update_xaxes(showspikes=True)
#     fig.update_yaxes(showspikes=True)

#     if search_date:
#         search_date = pd.to_datetime(search_date)
#         fig.update_xaxes(range=[search_date, ticker_data['Date'].iloc[-1]])

#     return fig

# @app.callback(
#     Output("stock-graph", "figure"),
#     [Input("ticker-dropdown", "value"),
#      Input("search-button", "n_clicks")],
#     [State('search-date', 'value')]
# )
# def update_graph(ticker, n_clicks, search_date):
#         return create_fig(ticker, search_date)

# if __name__ == '__main__':
#     app.run_server(debug=True)





import dash
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

df = pd.read_csv('full_data', parse_dates=['Date'])  # replace with your actual data file
app = Dash(__name__)


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
        yaxis1=dict(domain=[0.6, 1], anchor='x', title='Close', title_standoff=10),
        yaxis2=dict(domain=[0.45, 0.6], anchor='x', title='Volume', title_standoff=10),
        yaxis3=dict(domain=[0.3, 0.45], anchor='x', title='RSI', title_standoff=10),
        yaxis4=dict(domain=[0, 0.3], anchor='x', title='CCI', title_standoff=10),
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
