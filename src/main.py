from backtest import Backtest
from strategies import BollingerRSIStrategy, BollingerCCIStrategy, BuyAndHold
from summary import Summary
import numpy as np
from utils import adjust_types
from file_chooser import *
from uploadData import *


def run_backtest_on_ticker(data: pd.DataFrame, **backtest_kwargs):
    backtest = Backtest(data=data, **backtest_kwargs)
    return backtest.backtest()


def main(params=[0.0002, 100000, 1.0, 1]):
    input_dir = '../Data/Processed'
    # data_directory = input(
    #     "Enter the path of the directory containing data files or press enter for default: ")
    # input_name, _ = os.path.splitext(choose_file(data_directory))
    data = load_data_from_directory(input_dir)
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

    stop_loss = get_float_input("Enter Stop Loss (leave blank for 0.25)", 0.25)
    print(f"Stop Loss : {stop_loss}")

    rsi_high = get_float_input("Enter RSI High (leave blank for 62): ", 62)
    print(f"Rsi High : {rsi_high}")

    rsi_low = get_float_input("Enter RSI Low  (leave blank for 38): ", 38)
    print(f"Rsi Low Mul: {rsi_low}")

    cci_high = get_float_input("Enter CCI High  (leave blank for 100): ", 100)
    print(f"Cci High Mul: {cci_high}")

    cci_low = get_float_input("Enter CCI Low  (leave blank for -100): ", -100)
    print(f"Cci Low Mul: {cci_low}")

    print(f"Running backtest with params: {params}")
    ticker_groups = data.groupby("Ticker")

    backtest_results = {}
    # Create an empty DataFrame to store the combined results
    combined_results = pd.DataFrame()

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

    while True:
        file_name = input("Enter the name of the output file: ")
        if file_name != "":
            break
    output_directory = '../Data/Results/'
    combined_results.to_csv(f"{output_directory}{file_name}.csv", index=False)
    to_upload = input("Upload to S3? (y/n): ")
    if(to_upload == 'y'):
        upload_data_to_s3(combined_results, 'backtesting_results',
                      f"{file_name}.csv")


if __name__ == "__main__":
    main()
