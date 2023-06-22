from math import sqrt
import pandas as pd
import numpy as np
from uploadData import *
import pdb
from utils import adjust_types
from typing import Dict, Any
from simple_colors import red
from file_chooser import *


def calc_returns(srs, offset=1):
    returns = srs / srs.shift(offset) - 1.0
    return returns

class Summary:
    def __init__(self, data=None, ticker=None, strategy=None):
        self.ticker = ticker
        self.strategy = strategy
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
            self.avg_trade_return = None
            self.avg_trade_duration = None
            self.downside_deviation = None
            self.sortino = None
            self.best_trade = None
            self.worst_trade = None
            self.calmar_ratio = None
            self.number_of_trades = None
            self.positive_trades = None
            self.positive_trading_days = None


    def print_results(self):
        print("Strategy:", self.strategy)
        print(red("Total return:", "bold"), f"{self.total_return}%")
        if self.strategy.strip() != 'B&H':
            print(red("Sharpe:", "bold"), f"{self.sharpe}")
            print(red("Returns std:", "bold"), f"{self.returns_std}%")
        print(red("Max drawdown:", "bold"), f"{self.max_drawdown}%")
        print(red("Downside deviation:", "bold"), f"{self.downside_deviation}%")
        print(red("Number of trades:", "bold"), f"{self.number_of_trades}")
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
        # print('min balance', min_balance)
        # print('initial balance', initial_balance)

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
        # daily_returns_series = daily_returns_series.resample("24H").sum()
        # print('daily_returns_series', daily_returns_series)
        
        

        # print(f"Returns std: {self.returns_std}%")
        # total_return

        end_balance = data["Balance"].iloc[-1]
        total_return = ((end_balance - initial_balance) /
                        initial_balance) * 100
        self.total_return = round(total_return, 3)
        # print(f"Total return: {self.total_return}%")
        
        num_trading_days = len(daily_returns_series)
        # print('num_trading_days', num_trading_days)
        self.trading_days = num_trading_days
        
        # if (self.strategy == 'B&H'):
        #     df = data.copy()
        #     df["daily_returns"] = calc_returns(df["TP"])
        #     df["next_day_returns"] = df["daily_returns"].shift(-1)
        #     ret_series = df[['next_day_returns']].iloc[:, 0]
        #     std = ret_series.std() * 100
        #     print('std', std)
        #     sharpe = total_return / (std * sqrt(num_trading_days))
        #     print('sharpe', sharpe)
            
        daily_returns_series = daily_returns_series.dropna()
        self.number_of_trades = len(daily_returns_series)
        
        returns_std = daily_returns_series.std() * 100
        self.returns_std = round(returns_std, 3)

        
        
        self.sharpe = round(
        total_return / (returns_std * sqrt(num_trading_days)), 3
        )
        # print(f"Sharpe ratio: {self.sharpe}")


        # downside deviation
        # remove positive returns
        negative_returns_std = (
            daily_returns_series.apply(
                lambda x: x if x < 0 else np.nan).dropna()
        ).std() / sqrt(len(daily_returns_series))
        self.downside_deviation = round(negative_returns_std * 100, 3)

        # sortino - same as sharpe but using downside deviation instead of regular std
        self.sortino = round(total_return / negative_returns_std, 3)

        # best and worse trade
        self.best_trade = round(max(data["Return rate"].fillna(0)) * 100, 3)
        self.worst_trade = round(min(data["Return rate"].fillna(0)) * 100, 3)

        # Percentage of positive trades
        trades = data["Return rate"].dropna()
        profitable_trades = trades.apply(
            lambda x: x if x > 0 else np.nan).dropna()
        self.positive_trades = round(
            (len(profitable_trades) / len(trades)) * 100, 3)

        # profitable_days
        profitable_days = daily_returns_series.apply(
            lambda x: x if x > 0 else np.nan
        ).dropna()
        self.positive_trading_days = round(
            (len(profitable_days) / len(daily_returns_series)) * 100, 3
        )

    def get_results(self):
        res = {
            "Ticker": self.ticker,
            'Strategy': self.strategy,
            'Sharpe': self.sharpe,
            "Total return": self.total_return,
            "Max drawdown": self.max_drawdown,
            "Returns std": self.returns_std,
            "Downside deviation": self.downside_deviation,
            "Best trade": self.best_trade,
            "Worst trade": self.worst_trade,
            'Number of trades': self.number_of_trades,
            "Positive trades": self.positive_trades,
            "Positive trading days": self.positive_trading_days,
        }
        if self.strategy.strip() == 'B&H':
            res['Sharpe'] = 'N/A'
            res['Returns std'] = 'N/A'
            res['Max drawdown'] = 'N/A'

        
        return res


def main():
    input_dir = '../Data/Results'
    data = load_data_from_directory(input_dir)
    unique_tickers = data['Ticker'].unique()
    unique_strategies = data['Strategy'].unique()
    print(f"Unique Tickers: {unique_tickers}")
    print(f"Unique Strategies: {unique_strategies}")

    all_rows = []
    summary_results = {}
    for ticker in unique_tickers:
        summary_results[ticker] = {}
        for strategy in unique_strategies:
            ticker_strategy_data = data[(data["Ticker"] == ticker) & (
                data['Strategy'] == strategy)]
            if not ticker_strategy_data.empty:
                summary = Summary(ticker_strategy_data, ticker, strategy)
                summary_dict = summary.get_results()
                summary_dict['Ticker'] = ticker
                summary_dict['Strategy'] = strategy
                all_rows.append(summary_dict)
                print(
                    f"Summary results for Ticker: {ticker} and Strategy: {strategy}")
                summary.print_results()
                print("\n")

    df = pd.DataFrame(all_rows)
    output_name = input("Enter file name to save summary results: ")
    output_directory = '../Data/Summary/'
    output_path = f"{output_directory}/{output_name}.csv"
    df.to_csv(output_path, index=False)
    to_upload = input("Upload to S3? (y/n): ")
    if(to_upload == 'y'):
        upload_data_to_s3(df, 'summary_statistics', f"{output_name}.csv")


if __name__ == "__main__":

    main()
