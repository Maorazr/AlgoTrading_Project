import pandas as pd
import yfinance as yf
import numpy as np



def get_all_data(list, date1, date2):
    all_etf_data = pd.DataFrame()
    for tkr_str in list:
        single_df = yf.download(
            tickers=tkr_str, start=date1, end=date2, interval='1d', auto_adjust=True)
        single_df['Ticker'] = tkr_str
        all_etf_data = pd.concat([all_etf_data, single_df])
    all_etf_data = all_etf_data.reset_index()
    all_etf_data.to_csv('all_etf')
    return all_etf_data

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



def download_data_func(ticker_list_input, start_date, end_date):
    default_tickers = ['^GSPC', '^RUT', '^FCHI', '^IXIC', '^SSMI', '^NYA', '^STOXX', '^AEX', '^TA125.TA', 'TA35.TA', '^N225',
                '^HSI', '^STI']

    # If no tickers were provided, use the default list
    if ticker_list_input == 'none':
        ticker_list = default_tickers
        print(f"No tickers were provided, using the default list: {ticker_list}")
    else:
        try:
            ticker_list = parse_ticker_list(ticker_list_input)
            print(f"Using the following tickers: {ticker_list}")
        except Exception as e:
            print(f"Invalid input, please check your inputs. Error: {e}")
            return  # Exit the function
        
    try:
        # parse_date_range(start_date + end_date)
        print(f"You entered the following date range: {start_date} - {end_date}")
    except Exception as e:
        print(f"Invalid input, please check your inputs. Error: {e}")
        return  # Exit the function

    # Download the data
    etf_data = get_all_data(ticker_list, start_date, end_date)

    # Save the data to a CSV file
    etf_data.to_csv(f"../Data/OHLCV/{start_date} - {end_date}_OHLCV.csv")
