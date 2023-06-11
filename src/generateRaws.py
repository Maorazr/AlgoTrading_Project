

def generate_rows(ticker, strategy_summaries):
    ticker_strategy_keys = [
        key for key in strategy_summaries.keys() if key.startswith(ticker)]
    strategy_results = {
        key: strategy_summaries[key] for key in ticker_strategy_keys}
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
