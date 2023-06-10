import pandas as pd
import yfinance as yf
import numpy as np
from file_chooser import choose_file
import os


def get_all_data(list, date1, date2):
    all_etf_data = pd.DataFrame()
    for tkr_str in list:
        single_df = yf.download(tickers=tkr_str, start=date1, end=date2, interval='1d', auto_adjust=True)
        single_df['Ticker'] = tkr_str
        all_etf_data = pd.concat([all_etf_data, single_df])
    all_etf_data = all_etf_data.reset_index()
    all_etf_data.to_csv('all_etf')
    return all_etf_data


def calculate_sma(df, window_sizes=[20]):
    for w in window_sizes:
        df[f'SMA_{w}'] = df.groupby('Ticker')['TP'].transform(lambda x: x.rolling(window=w).mean())
    return df


def calculate_std(df, window_sizes=[20]):
    for w in window_sizes:
        df[f'STD_{w}'] = df.groupby('Ticker')['TP'].transform(lambda x: x.rolling(window=w).std())
    return df


def calculate_cci(data, params=[14, 0.015]):
    # Calculate the Typical Price (TP)
    data["TP"] = (data["High"] + data["Low"] + data["Close"]) / 3

    # Calculate the Moving Average of TP
    data["TP_SMA"] = data.groupby('Ticker')["TP"].transform(lambda x: x.rolling(window=params[0]).mean())

    # Calculate the Mean Deviation
    data["MD"] = data.groupby('Ticker')["TP"].transform(
        lambda x: x.rolling(window=params[0]).apply(lambda y: abs(y - y.mean()).mean()))

    # Calculate the CCI
    data["CCI"] = (data["TP"] - data["TP_SMA"]) / (params[1] * data["MD"])

    return data


def calculate_rsi(df, n=14):
    delta = df['TP'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(n).mean()
    avg_loss = loss.rolling(n).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df['RSI'] = rsi
    return df


def calculate_rsi_for_all_etfs(df, n=14):
    rsi_df_list = []
    for etf in df['Ticker'].unique():
        etf_df = df[df['Ticker'] == etf]
        rsi = calculate_rsi(etf_df, n)
        rsi_df = pd.DataFrame({'Ticker': etf_df['Ticker'], 'Date': etf_df['Date'], 'RSI': rsi})
        rsi_df_list.append(rsi_df)
    rsi_df = pd.concat(rsi_df_list, ignore_index=True)
    return rsi_df


def makeit(df, params=[[20], [20], [14, 0.015], 14]):
    df = calculate_cci(df, params[2])
    df = calculate_sma(df, params[0])
    df = calculate_std(df, params[1])

    modified_dfs = []
    for etf in df['Ticker'].unique():
        etf_df = df[df['Ticker'] == etf].copy()
        etf_df = calculate_rsi(etf_df, params[3])  # This will add RSI column to etf_df
        modified_dfs.append(etf_df)

    df = pd.concat(modified_dfs, ignore_index=True)
    df = df.dropna().reset_index(drop=True)
    sma_period = params[0][0]
    std_period = params[1][0]
    df["BU"] = df[f'SMA_{sma_period}'] + df[f'STD_{std_period}'] * 2
    df["BL"] = df[f'SMA_{sma_period}'] - df[f'STD_{std_period}'] * 2
    return df.copy()


def validated_input(prompt, validation_fn, *args):
    while True:
        try:
            value = input(prompt)
            return validation_fn(value, *args)
        except Exception as e:
            print(f"Invalid input, please try again. Error: {e}")


def parse_ticker_list(value, etf_list):
    if value.strip() == '':
        return etf_list
    else:
        return [ticker.strip().upper() for ticker in value.split(',')]


def parse_date_range(value):
    start_date, end_date = value.split(',')
    return start_date.strip(), end_date.strip()


def parse_int_list(value):
    return [int(w.strip()) for w in value.split(',')]


def parse_cci_params(value):
    cci_period, cci_std = map(float, value.split(','))
    return [int(cci_period), cci_std]


def parse_rsi_window(value):
    return int(value.strip())


def main():
    etf_list = ['^GSPC', '^RUT', '^FCHI', '^IXIC', '^SSMI', '^NYA', '^STOXX', '^AEX', '^TA125.TA', 'TA35.TA', '^N225',
                '^HSI', '^STI']

    download_data = input("Do you want to download data? (y/n): ")
    if download_data.lower() == 'y':
        ticker_list = validated_input("Please enter a list of tickers separated by commas (leave blank for default): ",
                                      parse_ticker_list, etf_list)
        print(f"Using the following tickers: {ticker_list}")
        start_date, end_date = validated_input("Please enter start and end dates (YYYY-MM-DD,YYYY-MM-DD): ",
                                               parse_date_range)
        print(f"You entered the following date range: {start_date} - {end_date}")
        etf_data = get_all_data(ticker_list, start_date, end_date)
        etf_data.to_csv(f"../Data/OHLCV/{start_date} - {end_date}_OHLCV.csv")

    else:
        processe_data = input('Do you want to open file from home directory? (y/n): ')
        if processe_data.lower() == 'y':
            data_directory = input("Enter the path of the directory containing data files: ")
            chosen_file = choose_file(data_directory)
            input_name, _ = os.path.splitext(chosen_file)
            etf_data = pd.read_csv(os.path.join(data_directory, f"{input_name}.csv"))
        else:
            return True

    # etf_data = get_all_data(ticker_list, start_date, end_date)
    # etf_data.to_csv("../Data/etf_data.csv")

    sma_windows = validated_input("Please enter a list of SMA windows separated by commas: ", parse_int_list)
    print(f"You entered the following SMA windows: {sma_windows}")

    std_windows = validated_input("Please enter a list of STD windows separated by commas: ", parse_int_list)
    print(f"You entered the following STD windows: {std_windows}")

    cci_params = validated_input("Please enter a list of CCI parameters separated by commas period,std : ",
                                 parse_cci_params)
    print(f"You entered the following CCI parameters: {cci_params}")

    rsi_window = validated_input("Please enter a RSI window: ", parse_rsi_window)
    print(f"You entered the following RSI window: {rsi_window}")

    params = [sma_windows, std_windows, cci_params, rsi_window]
    print(f"Using the following parameters: {params}")
    file_name = input("Please enter a file name: ")
    makeit(etf_data, params).to_csv(f"../Data/Processed/{file_name}.csv")


if __name__ == '__main__':
    main()
