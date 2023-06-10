from temp import *


def res_data(ticker_data, ticker, entry_points, exit_points, selected_indicators):
    sma_column = find_sma_column(ticker_data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=entry_points['Date'],
                             y=entry_points['Close'],
                             mode='markers',
                             marker=dict(color='green', opacity=0.5, size=12),
                             name='Entry'))

    fig.add_trace(go.Scatter(x=exit_points['Date'],
                             y=exit_points['Close'],
                             mode='markers',
                             marker=dict(color='red', opacity=0.5, size=12),
                             name='Exit'))

    fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', line=dict(color='#6495ED'),
                             name='Close', yaxis='y1'))
    fig.add_trace(
        go.Scatter(x=ticker_data['Date'], y=ticker_data['BU'], line=dict(color='green'), name='BU', yaxis='y1'))
    fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['BL'], line=dict(
        color='red'), name='BL', yaxis='y1'))
    fig.add_trace(
        go.Scatter(x=ticker_data['Date'], y=ticker_data[sma_column], line=dict(color='orange'), name=sma_column,
                   yaxis='y1'))
    # fig = common_traces(ticker_data, ticker, fig)
    if 'RSI' in selected_indicators:
        fig.add_trace(
            go.Scatter(x=ticker_data['Date'], y=ticker_data['RSI'], line=dict(color='blue'), name='RSI', yaxis='y2'))
    if 'CCI' in selected_indicators:
        fig.add_trace(
            go.Scatter(x=ticker_data['Date'], y=ticker_data['CCI'], line=dict(color='purple'), name='CCI', yaxis='y3'))
    if 'Volume' in selected_indicators:
        fig.add_trace(go.Bar(
            x=ticker_data['Date'], y=ticker_data['Volume'], showlegend=False, yaxis='y4'))

    # Update y-axis domains based on selected indicators
    num_selected_indicators = len(selected_indicators)

    if num_selected_indicators == 3:
        y1_domain = [0.5, 1]
        y2_domain = [0.3, 0.45]
        y3_domain = [0.10, 0.28]
        y4_domain = [0, 0.09]
    elif num_selected_indicators == 2:
        if 'RSI' not in selected_indicators:
            y1_domain = [0.32, 1]
            y2_domain = [0, 0]
            y3_domain = [0.10, 0.28]
            y4_domain = [0, 0.09]
        elif 'CCI' not in selected_indicators:
            y1_domain = [0.32, 1]
            y2_domain = [0.10, 0.28]
            y3_domain = [0, 0]
            y4_domain = [0, 0.09]
        elif 'Volume' not in selected_indicators:
            y1_domain = [0.35, 1]
            y2_domain = [0.15, 0.30]
            y3_domain = [0.0, 0.14]
            y4_domain = [0, 0]
    elif num_selected_indicators == 1:
        if 'RSI' and 'CCI' not in selected_indicators:
            y1_domain = [0.2, 1]
            y2_domain = [0, 0]
            y3_domain = [0, 0]
            y4_domain = [0, 0.09]
        elif 'RSI' and 'Volume' not in selected_indicators:
            y1_domain = [0.2, 1]
            y2_domain = [0, 0]
            y3_domain = [0, 0.15]
            y4_domain = [0, 0]
        elif 'CCI' and 'Volume' not in selected_indicators:
            y1_domain = [0.3, 1]
            y2_domain = [0.1, 0.28]
            y3_domain = [0, 0]
            y4_domain = [0, 0]
    else:
        y1_domain = [0, 1]
        y2_domain = [0, 0]
        y3_domain = [0, 0]
        y4_domain = [0, 0]

    fig.update_layout(
        plot_bgcolor='rgba(240, 240, 240, 0.5)',
        paper_bgcolor='rgba(240, 240, 240, 0.5)',
        height=900,
        title=f'Ticker: {ticker}',
        hovermode='x unified',
        yaxis1=dict(domain=y1_domain, anchor='x',
                    title='Close', title_standoff=10),
        # yaxis1=dict(domain=[0.5, 1], anchor='x', title='Close', title_standoff=10),
        yaxis2=dict(domain=y2_domain, anchor='x',
                    title='RSI', title_standoff=10),
        yaxis3=dict(domain=y3_domain, anchor='x',
                    title='CCI', title_standoff=10),
        yaxis4=dict(domain=y4_domain, anchor='x',
                    title='Volume', title_standoff=10),
        xaxis=dict(domain=[0, 1]),
    )
    fig.update_xaxes(showgrid=True, gridwidth=1,
                     gridcolor='LightGrey', dtick='M3')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')

    return fig
