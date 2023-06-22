from temp import common_traces
import plotly.graph_objects as go


def origin_data(ticker_data, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ticker_data['Date'], y=ticker_data['TP'], mode='lines', name='Adj Close', yaxis='y1'))
    fig = common_traces(ticker_data, ticker, fig)
    fig.update_layout(
        plot_bgcolor='rgba(240, 240, 240, 0.5)',
        paper_bgcolor='rgba(240, 240, 240, 0.5)',
        height=900,
        title=f'Ticker: {ticker}',
        hovermode='x unified',
        yaxis1=dict(domain=[0.5, 1], anchor='x',
                    title='Close', title_standoff=10),
        yaxis2=dict(domain=[0.30, 0.45], anchor='x',
                    title='RSI', title_standoff=10),
        yaxis3=dict(domain=[0.10, 0.28], anchor='x',
                    title='CCI', title_standoff=10),
        yaxis4=dict(domain=[0, 0.09], anchor='x',
                    title='Volume', title_standoff=10),
        xaxis=dict(domain=[0, 1]),
    )
    fig.update_xaxes(showgrid=True, gridwidth=1,
                     gridcolor='LightGrey', dtick='M3')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')

    return fig
