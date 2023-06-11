
from io import StringIO
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, dash, callback
from dash import register_page
from temp import *
from getFiles import *




register_page(__name__)
global strategy_summaries

global file_names
file_names = get_names('summary_statistics')

strategy_summaries = get_default_file('summary_statistics/testing.csv', 'json')

layout = html.Div([
    dcc.Dropdown(
        id='selected-files-dropdown-statistics',
        options=file_names,
        multi=False,
    ),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker}
                 for ticker in strategy_summaries['Ticker'].unique()],
        value=strategy_summaries['Ticker'].unique()[0]
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
              ), html.Div(id='file-output-statistics')])


@callback(
    Output('file-output-statistics', 'children'),
    Input('selected-files-dropdown-statistics', 'value')
)
def update_output(selected_file):
    if selected_file:
        file_path = f"summary_statistics/{selected_file}"
        s3 = boto3.client('s3', aws_access_key_id='AKIA4C5ZLMSXERDLI3HV',
                          aws_secret_access_key='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')
        obj = s3.get_object(Bucket=bucket_name, Key=file_path)
        global strategy_summaries
        csv_data = obj['Body'].read().decode('utf-8')
        strategy_summaries = pd.read_csv(StringIO(csv_data))
        print('strategy_summaries')
        print(strategy_summaries)
    else:
        return 'Please select a file'



def create_fig(ticker):
    fig = stats_data(ticker)
    return fig


@callback(
    Output("stock-graph-statistics", "figure"),
    [Input("ticker-dropdown", "value"),
     Input('selected-files-dropdown-statistics', 'value')]
)
def update_graph(ticker, selected_file):
    return create_fig(ticker)


def stats_data(ticker):
    # rows = generate_rows(ticker, strategy_summaries)
    # stats_df = pd.DataFrame(rows)
    # print(stats_df)

    stats_df = strategy_summaries[strategy_summaries['Ticker'] == ticker]

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
