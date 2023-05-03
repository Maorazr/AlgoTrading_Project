import pandas as pd
import yfinance as yf
import numpy as np


def get_all_data(list, date1, date2):
    all_etf_data = pd.DataFrame()
    for tkr_str in list:
        single_df = yf.download(tickers=tkr_str, start=date1, end=date2,interval='1d', auto_adjust=True)
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
    df["BU"] = df['SMA_20'] + df['STD_20']*2
    df["BL"] = df['SMA_20'] - df['STD_20']*2
    return df.copy()


def main():
    etf_list = ['^RUT', '^GSPC', '^STI', '^FCHI', '^HSI', '^NYA', '^AEX', '^TA125.TA', 'TA35.TA', '^N225', '^SSMI',
                '^IXIC', '^STOXX']
    ticker_list = input("Please enter a list of tickers separated by commas (leave blank for default): ")
    if ticker_list.strip() == '':
        ticker_list = etf_list
    else:
        ticker_list = ticker_list = [ticker.strip().upper() for ticker in ticker_list.split(',')]

    print(f"Using the following tickers: {ticker_list}")

    start_date, end_date = input("Please enter start and end dates (YYYY-MM-DD,YYYY-MM-DD): ").split(',')
    start_date = start_date.strip()
    end_date = end_date.strip()
    print(f"You entered the following date range: {start_date} - {end_date}")
    etf_data = get_all_data(ticker_list, start_date, end_date)
    etf_data.to_csv("../Data/etf_data.csv")

    sma_windows = input("Please enter a list of SMA windows separated by commas: ")
    sma_windows = [int(w.strip()) for w in sma_windows.split(',')]
    print(f"You entered the following SMA windows: {sma_windows}")

    std_windows = input("Please enter a list of STD windows separated by commas: ")
    std_windows = [int(w.strip()) for w in std_windows.split(',')]
    print(f"You entered the following STD windows: {std_windows}")

    cci_period, cci_std = map(float,
                              input("Please enter a list of CCI parameters separated by commas period,std : ").split(
                                  ','))
    cci_period = int(cci_period)
    cci_params = [cci_period, cci_std]
    print(f"You entered the following CCI parameters: {cci_params}")

    rsi_window = input("Please enter a RSI window: ")
    rsi_window = int(rsi_window.strip())
    print(f"You entered the following RSI window: {rsi_window}")

    params = [sma_windows, std_windows, cci_params, rsi_window]
    print(f"Using the following parameters: {params}")
    file_name = input("Please enter a file name: ")
    makeit(etf_data, params).to_csv(f"../Data/{file_name}.csv")



if __name__ == '__main__':
    main()

