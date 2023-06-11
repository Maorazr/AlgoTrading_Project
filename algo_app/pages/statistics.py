
from io import StringIO
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, dash, callback
from dash import register_page
from temp import *
from getFiles import *


register_page(__name__)
global strategy_summaries

strategy_summaries = get_default_file('0.1stop_stats.json', 'json')
layout = html.Div([
    dcc.Dropdown(
        id='data-type-dropdown',
        options=[{'label': data_type, 'value': data_type}
                 for data_type in ['Stats']],
        value='Stats'
    ),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker}
                 for ticker in strategy_summaries.keys()],
        value=list(strategy_summaries.keys())[0]
    ),
    dcc.Graph(id='stock-graph-statistics',
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
              )
])


def create_fig(ticker):
    fig = stats_data(ticker)
    return fig


@callback(
    Output("stock-graph-statistics", "figure"),
    [Input("ticker-dropdown", "value")]
)
def update_graph(ticker):
    return create_fig(ticker)


def stats_data(ticker):
    rows = generate_rows(ticker, strategy_summaries)
    stats_df = pd.DataFrame(rows)

    stats_df_vertical = stats_df.set_index('Strategy').T
    stats_df_vertical.columns = [col.replace(
        ticker + '_', '') for col in stats_df_vertical.columns]

    fig = go.Figure()

    sharpe_colors = ['#A9A9A9', '#6495ED', '#E9967A']
    total_return_colors = ['#B8860B', '#FF8C00', 'lightblue']

    fig.add_trace(go.Bar(
        x=stats_df_vertical.columns,
        y=stats_df_vertical.loc['Sharpe'],
        name='Sharpe',
        orientation='v',
        marker=dict(color=sharpe_colors),
        opacity=0.7,
        showlegend=True,
        legendrank=1,
        text=stats_df_vertical.loc['Sharpe'],
        textposition='auto',
        texttemplate='%{text:.2f}',
        textfont=dict(size=16),
        xaxis='x2',
        yaxis='y2'
    ))

    fig.add_trace(go.Bar(
        x=stats_df_vertical.columns,
        y=stats_df_vertical.loc['Total return'],
        name='Total Return',
        orientation='v',
        marker=dict(color=total_return_colors),
        opacity=0.7,
        text=stats_df_vertical.loc['Total return'],
        textposition='auto',
        texttemplate='%{text:.2f}',
        textfont=dict(size=16),
        xaxis='x3',
        yaxis='y3'
    ))

    fig.add_trace(go.Table(
        header=dict(values=['Parameters'] + stats_df_vertical.columns[0:].tolist(),
                    fill_color='lightskyblue',
                    align='left',
                    font=dict(size=18, color='black')),
        cells=dict(values=[stats_df_vertical.index] + [stats_df_vertical[col] for col in stats_df_vertical.columns],
                   fill_color='lightgray',
                   align='left',
                   font=dict(size=16, color='black'),
                   height=35),
        columnwidth=[0.4, 0.4, 0.4, 0.4],
        domain=dict(x=[0, 0.3], y=[0, 1])
    ))

    fig.update_layout(
        height=600,
        xaxis2=dict(domain=[0.35, 0.65], anchor='x2'),
        yaxis2=dict(domain=[0, 1], anchor='y2'),
        xaxis3=dict(domain=[0.7, 1], anchor='x3'),
        yaxis3=dict(domain=[0, 1], anchor='y3'),
        margin=dict(l=20, r=20, t=50, b=0),
    )

    return fig
