from datetime import datetime as datetime
import pandas as pd


def adjust_types(data: pd.DataFrame) -> pd.DataFrame:
    data["Date"] = pd.to_datetime(data["Date"])
    data["Open"] = data["Open"].astype(float)
    data["High"] = data["High"].astype(float)
    data["Low"] = data["Low"].astype(float)
    data["Close"] = data["Close"].astype(float)
    data["Volume"] = data["Volume"].astype(int)
    data["Ticker"] = data["Ticker"].astype(str)
    return data



def add_zero(st):
    """
    :param st: a string with datetime
    :return: the same string with "0" before the hour if needed
    """
    splited = st.split(" ")
    return splited[0] + " 0" + splited[1]
