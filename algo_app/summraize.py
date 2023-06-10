from temp import *
from app import strategy_summaries, strategy_summaries2


def summraize(ticker):
    rows1 = generate_rows(ticker, strategy_summaries)
    stats_df1 = pd.DataFrame(rows1)

    rows2 = generate_rows(ticker, strategy_summaries2)
    stats_df2 = pd.DataFrame(rows2)

    stats_df1_vertical = stats_df1.set_index('Strategy').T
    stats_df2_vertical = stats_df2.set_index('Strategy').T
    stats_df1_vertical.columns = [col.replace(
        ticker + '_', '') for col in stats_df1_vertical.columns]
    stats_df2_vertical.columns = [col.replace(
        ticker + '_', '') for col in stats_df2_vertical.columns]
    # fig = go.Figure()
    fig = make_subplots(rows=2, cols=3, specs=[
                        [{'type': 'table'}, {'type': 'xy'}, {'type': 'xy'}]] * 2, )

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
        text="Total return",
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
        y=stats_df2_vertical.loc['Total return'],
        name='Default ret',
        orientation='v',
        opacity=0.7,
        width=0.38,
        text=stats_df2_vertical.loc['Total return'],
        textposition='auto',
        texttemplate='%{text:.2f}',
        textfont=dict(size=16),
    ), row=1, col=3)

    fig.add_trace(go.Bar(
        x=stats_df1_vertical.columns,
        y=stats_df1_vertical.loc['Total return'],
        name='Optimized ret',
        orientation='v',
        marker=dict(color=total_return_colors),
        width=0.38,
        opacity=0.7,
        text=stats_df1_vertical.loc['Total return'],
        textposition='auto',
        texttemplate='%{text:.2f}',
        textfont=dict(size=16),
    ), row=1, col=3)

    fig.add_trace(go.Bar(
        x=stats_df2_vertical.columns,
        y=stats_df2_vertical.loc['Total return'],
        name='Default ret',
        orientation='v',
        marker=dict(color=total_return_colors),
        width=0.38,
        opacity=0.7,
        text=stats_df2_vertical.loc['Total return'],
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
