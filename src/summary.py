from math import sqrt
import pandas as pd
import numpy as np

import pdb
from utils import adjust_types
from typing import Dict, Any
import json
from simple_colors import red
from file_chooser import choose_file
import os

class Summary:
    def __init__(self, data=None):
        if data is not None:
            if not isinstance(data.index, pd.DatetimeIndex):
                data.index = pd.to_datetime(data['Date'])

            self.init(data)
        else:
            self.max_balance_drowdown = None
            self.max_drawdown = None
            self.returns_std = None
            self.total_return = None
            self.sharpe = None
            self.downside_deviation = None
            self.sortino = None
            self.best_trade = None
            self.worst_trade = None
            self.calmar_ratio = None
            self.positive_trades = None
            self.positive_trading_days = None


    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Summary':
        summary = cls()
        summary.total_return = data['Total return']
        summary.sharpe = data['Sharpe']
        summary.sortino = data['Sortino']
        summary.max_balance_drowdown = data['Max balance drawdown']
        summary.max_drawdown = data['Max drawdown']
        summary.returns_std = data['Returns std']
        summary.downside_deviation = data['Downside deviation']
        summary.best_trade = data['Best trade']
        summary.worst_trade = data['Worst trade']
        summary.positive_trades = data['Positive trades']
        summary.positive_trading_days = data['Positive trading days']
        return summary



    
    def print_results(self):
        print(red("Total return:", "bold"), f"{self.total_return}%")
        print(red("Sharpe:", "bold"), f"{self.sharpe}")
        print(red("Sortino:", "bold"), f"{self.sortino}%")
        print(red("Max balance drawdown:", "bold"), f"{self.max_balance_drowdown}%")
        print(red("Max drawdown:", "bold"), f"{self.max_drawdown}%")
        print(red("Returns std:", "bold"), f"{self.returns_std}%")
        print(red("Downside deviation:", "bold"), f"{self.downside_deviation}%")
        print(red("Best trade:", "bold"), f"{self.best_trade}%")
        print(red("Worst trade:", "bold"), f"{self.worst_trade}%")
        print(red("Positive trades:", "bold"), f"{self.positive_trades}%")
        print(red("Positive trading days:", "bold"), f"{self.positive_trading_days}%")

    def init_from_csv(self, csv_path):
        data = pd.read_csv(csv_path)
        data = adjust_types(data)
        self.init(data)

    def init(self, data):
        if 'Return rate' not in data.columns:
            data['Return rate'] = 0
        # max_balance_drowdown
        min_balance = min(data["Balance"])
        initial_balance = data["Balance"].iloc[0]
        self.max_balance_drowdown = round(
            (1 - (min_balance / initial_balance)) * 100, 3
        )

        # returns_std, convert to a series
        daily_returns_series = data[['Return rate']].iloc[:, 0]

        # max drawdown
        cumulative_max = daily_returns_series.cummax()
        drawdown = cumulative_max - daily_returns_series
        self.max_drawdown = round(drawdown.max() * 100, 3)
        # resample by day to get daily return
        daily_returns_series = daily_returns_series.resample("24H").sum()
        returns_std = daily_returns_series.std() * 100
        self.returns_std = round(returns_std, 3)

        # total_return
        end_balance = data["Balance"].iloc[-1]
        total_return = ((end_balance - initial_balance) / initial_balance) * 100
        self.total_return = round(total_return, 3)

        # sharpe ratio = total return percentage / standard deviation * sqrt(num of trading days)
        self.sharpe = round(
            total_return / (returns_std * sqrt(len(daily_returns_series))), 3
        )

        # downside deviation
        # remove positive returns
        negative_returns_std = (
            daily_returns_series.apply(lambda x: x if x < 0 else np.nan).dropna()
        ).std() / sqrt(len(daily_returns_series))
        self.downside_deviation = round(negative_returns_std * 100, 3)

        # sortino - same as sharpe but using downside deviation instead of regular std
        self.sortino = round(total_return / negative_returns_std, 3)

        # best and worse trade
        self.best_trade = round(max(data["Return rate"].fillna(0)) * 100, 3)
        self.worst_trade = round(min(data["Return rate"].fillna(0)) * 100, 3)

        # Percentage of positive trades
        trades = data["Return rate"].dropna()
        profitable_trades = trades.apply(lambda x: x if x > 0 else np.nan).dropna()
        self.positive_trades = round((len(profitable_trades) / len(trades)) * 100, 3)

        # profitable_days
        profitable_days = daily_returns_series.apply(
            lambda x: x if x > 0 else np.nan
        ).dropna()
        self.positive_trading_days = round(
            (len(profitable_days) / len(daily_returns_series)) * 100, 3
        )

    def get_results(self):
            return {
                "Total return": self.total_return,
                "Sharpe": self.sharpe,
                "Sortino": self.sortino,
                "Max balance drawdown": self.max_balance_drowdown,
                "Max drawdown": self.max_drawdown,
                "Returns std": self.returns_std,
                "Downside deviation": self.downside_deviation,
                "Best trade": self.best_trade,
                "Worst trade": self.worst_trade,
                "Positive trades": self.positive_trades,
                "Positive trading days": self.positive_trading_days,
            }


def main():

    data_directory = input("Enter the path of the directory containing data files: ")
    input_name, _ = os.path.splitext(choose_file(data_directory))
    data = pd.read_csv(os.path.join(data_directory, f"{input_name}.csv"))
    unique_tickers = data['Ticker'].unique()
    unique_strategies = data['Strategy'].unique()

    summary_results = {}
    for ticker in unique_tickers:
        summary_results[ticker] = {}
        for strategy in unique_strategies:
            ticker_strategy_data = data[(data["Ticker"] == ticker) & (data['Strategy'] == strategy)]
            summary = Summary(ticker_strategy_data)
            summary_results[f"{ticker}_{strategy}"] = summary.get_results()
            print(f"Summary results for Ticker: {ticker} and Strategy: {strategy}")
            summary.print_results()
            print("\n")
    output_name = input("Enter file name to save summary results: ")
    output_directory = "output"  # Change this to the desired folder
    output_path = f"../results/Json_stat/{output_name}.json"
    with open(output_path, "w") as outfile:
        json.dump(summary_results, outfile, indent=4)


if __name__ == "__main__":

    main()
