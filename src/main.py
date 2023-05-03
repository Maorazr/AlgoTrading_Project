import json
import pdb
import os
import pandas as pd
from backtest import Backtest
from strategies import BollingerRSIStrategy, BollingerCCIStrategy, BuyAndHold
from summary import Summary
import numpy as np
from utils import adjust_types


def choose_file(directory=None):
    files = list_files_in_directory(directory)

    # ... (rest of the code)


    print("Select a file by entering its number:")

    for index, file_name in enumerate(files, start=1):
        print(f"{index}: {file_name}")

    while True:
        try:
            user_choice = int(input("Enter the number of the desired file: "))
            if 1 <= user_choice <= len(files):
                chosen_file = files[user_choice - 1]
                print(f"You have chosen: {chosen_file}")
                return chosen_file
            else:
                print("Invalid number. Please choose a number from the list.")
        except ValueError:
            print("Please enter a valid number.")


def list_files_in_directory(directory=None):
    if directory is None:
        directory = os.getcwd()
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files


def run_backtest_on_ticker(data: pd.DataFrame, **backtest_kwargs):
    backtest = Backtest(data=data, **backtest_kwargs)
    return backtest.backtest()


def main(params=[0.0002, 100000, 1.0, 1]):
    data_directory = input("Enter the path of the directory containing data files: ")
    input_name, _ = os.path.splitext(choose_file(data_directory))
    data = pd.read_csv(os.path.join(data_directory, f"{input_name}.csv"))
    data = adjust_types(data)
    temp = input(
        "Enter array of params separated with commas commission, balance, leverage, buy_percentage (leave blank for default): ")
    if temp != "":
        params = np.array(temp.split(",")).astype(float)

    def get_float_input(prompt, default_value):
        user_input = input(prompt)
        if user_input != "":
            return float(user_input)
        else:
            return default_value

    rsi_high_mul = get_float_input("Enter RSI High multiplier (leave blank for default): ", 1)
    print(f"Rsi High Mul: {rsi_high_mul}")

    rsi_low_mul = get_float_input("Enter RSI Low multiplier (leave blank for default): ", 1)
    print(f"Rsi Low Mul: {rsi_low_mul}")

    cci_high_mul = get_float_input("Enter CCI High multiplier (leave blank for default): ", 1)
    print(f"Cci High Mul: {cci_high_mul}")

    cci_low_mul = get_float_input("Enter CCI Low multiplier (leave blank for default): ", 1)
    print(f"Cci Low Mul: {cci_low_mul}")

    print(f"Running backtest with params: {params}")
    ticker_groups = data.groupby("Ticker")

    backtest_results = {}
    combined_results = pd.DataFrame()  # Create an empty DataFrame to store the combined results

    for ticker, ticker_data in ticker_groups:
        print(f"Running backtest on {ticker}...")

        # BollingerRSIStrategy
        bollinger_rsi_results = run_backtest_on_ticker(
            data=ticker_data,
            commission=params[0],
            balance=params[1],
            strategy=BollingerRSIStrategy(rsi_high_mul, rsi_low_mul),
            leverage=params[2],
            window_size=100,
            buy_percentage=params[3],
        )

        # BollingerCCIStrategy
        bollinger_cci_results = run_backtest_on_ticker(
            data=ticker_data,
            commission=params[0],
            balance=params[1],
            strategy=BollingerCCIStrategy(cci_high_mul, cci_low_mul),
            leverage=params[2],
            window_size=100,
            buy_percentage=params[3],
        )

        buy_and_hold_results = run_backtest_on_ticker(
            data=ticker_data,
            commission=params[0],
            balance=params[1],
            strategy=BuyAndHold(),
            leverage=params[2],
            window_size=100,
            buy_percentage=params[3],
        )

        backtest_results[ticker] = {
            "BollingerRSIStrategy": bollinger_rsi_results,
            "BollingerCCIStrategy": bollinger_cci_results,
        }
        backtest_results[ticker]["BuyAndHold"] = buy_and_hold_results
        # Use pd.concat() to combine the results for each ticker and strategy
        combined_results = pd.concat([combined_results, bollinger_rsi_results])
        combined_results = pd.concat([combined_results, bollinger_cci_results])
        combined_results = pd.concat([combined_results, buy_and_hold_results])
    # Reset the index of the combined_results DataFrame
    combined_results.reset_index(drop=True, inplace=True)

    with open('strategy_summaries.json', 'w') as f:
        json.dump({}, f)

    strategy_summaries = {}
    # Recreate Summary objects from the loaded data
    for ticker, ticker_data in ticker_groups:
        # Generate the Summary objects for each strategy
        bollinger_rsi_summary = Summary(bollinger_rsi_results).print_results
        bollinger_cci_summary = Summary(bollinger_cci_results).print_results
        buy_and_hold_summary = Summary(buy_and_hold_results).print_results
        strategy_summaries[ticker] = {
            "BollingerRSIStrategy": bollinger_rsi_summary,
            "BollingerCCIStrategy": bollinger_cci_summary,
            "BuyAndHold": buy_and_hold_summary,
        }
        with open('strategy_summaries.json', 'r') as f:
            strategy_summaries_data = json.load(f)
    # Save the combined_results DataFrame to a CSV file
    for ticker, results in backtest_results.items():
        print(f"\nResults for {ticker}:")
        for strategy_name, strategy_results in results.items():
            print(f"{strategy_name} Results:")
            summary = Summary(
                strategy_results
            )  # Create a summary object for each strategy's results
            summary.print_results()  # Print the summary
    file_name = input("Enter file name to save results: ")
    combined_results.to_csv(f"../results/{file_name}.csv", index=False)


if __name__ == "__main__":
    main()
