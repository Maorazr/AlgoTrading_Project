import json
import pdb
import os
import pandas as pd
from backtest import Backtest
from strategies import BollingerRSIStrategy, BollingerCCIStrategy, BuyAndHold
from summary import Summary
import numpy as np
from utils import adjust_types
from file_chooser import choose_file




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
    
    stop_loss = get_float_input("Enter Stop Loss (leave blank for 0.1)", 0.1)
    print(f"Stop Loss : {stop_loss}")

    rsi_high = get_float_input("Enter RSI High (leave blank for 70): ", 70)
    print(f"Rsi High : {rsi_high}")

    rsi_low = get_float_input("Enter RSI Low  (leave blank for 30): ", 30)
    print(f"Rsi Low Mul: {rsi_low}")

    cci_high = get_float_input("Enter CCI High  (leave blank for 100): ", 100)
    print(f"Cci High Mul: {cci_high}")

    cci_low = get_float_input("Enter CCI Low  (leave blank for -100): ", -100)
    print(f"Cci Low Mul: {cci_low}")

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
            strategy=BollingerRSIStrategy(rsi_high, rsi_low, stop_loss),
            leverage=params[2],
            window_size=20,
            buy_percentage=params[3],
        )

        # BollingerCCIStrategy
        bollinger_cci_results = run_backtest_on_ticker(
            data=ticker_data,
            commission=params[0],
            balance=params[1],
            strategy=BollingerCCIStrategy(cci_high, cci_low, stop_loss),
            leverage=params[2],
            window_size=20,
            buy_percentage=params[3],
        )

        buy_and_hold_results = run_backtest_on_ticker(
            data=ticker_data,
            commission=params[0],
            balance=params[1],
            strategy=BuyAndHold(),
            leverage=params[2],
            window_size=20,
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


    strategy_summaries = {}
    # Recreate Summary objects from the loaded data
    for ticker, ticker_data in ticker_groups:
        # Generate the Summary objects for each strategy
        # bollinger_rsi_summary = Summary(bollinger_rsi_results).print_results
        # bollinger_cci_summary = Summary(bollinger_cci_results).print_results
        # buy_and_hold_summary = Summary(buy_and_hold_results).print_results
        bollinger_rsi_summary = str(Summary(bollinger_rsi_results).print_results)
        bollinger_cci_summary = str(Summary(bollinger_cci_results).print_results)
        buy_and_hold_summary = str(Summary(buy_and_hold_results).print_results)
        strategy_summaries[ticker] = {
            "BollingerRSIStrategy": bollinger_rsi_summary,
            "BollingerCCIStrategy": bollinger_cci_summary,
            "BuyAndHold": buy_and_hold_summary,
        }

    # with open('strategy_summaries.json', 'w') as f:
    #     json.dump(strategy_summaries, f)
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
