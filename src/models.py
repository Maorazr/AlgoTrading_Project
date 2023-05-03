from abc import ABCMeta, abstractmethod
import pandas as pd
from enum import Enum


class OrderType(Enum):
    OPEN_LONG = 1
    OPEN_SHORT = 2
    CLOSE_LONG = 3
    CLOSE_SHORT = 4


class PositionSide(Enum):
    LONG = 1
    SHORT = 2


class BrokerInstruction:
    def __init__(self, order_type: OrderType, price: float):
        self.order_type = order_type
        self.price = price



class Position:
    def __init__(self, qty: float, entry_price: float, side: PositionSide):
        self.qty = qty
        self.entry_price = entry_price
        self.side = side
        self.low = entry_price
        self.high = entry_price

    

class Strategy(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name

    def enter_position(self, data: pd.DataFrame) -> BrokerInstruction:
        raise NotImplementedError

    @abstractmethod
    def exit_position(
        self, data: pd.DataFrame, position: Position
    ) -> BrokerInstruction:
        raise NotImplementedError


class BollingerBandsRSI(Strategy):
    def __init__(self, rsi_period=14, rsi_low=30, rsi_high=70, name='BbRSI'):
        self.rsi_period = rsi_period
        self.rsi_low = rsi_low
        self.rsi_high = rsi_high

    def enter_position(self, data: pd.DataFrame) -> BrokerInstruction:
        # Your Bollinger Bands RSI strategy logic
        pass

    def exit_position(self, data: pd.DataFrame, position: Position) -> BrokerInstruction:
        # Your Bollinger Bands RSI strategy exit logic
        pass


class BollingerBandsCCI(Strategy):
    def __init__(self, cci_period=20, cci_low=-100, cci_high=100, name='BbCCI'):
        self.cci_period = cci_period
        self.cci_low = cci_low
        self.cci_high = cci_high

    def enter_position(self, data: pd.DataFrame) -> BrokerInstruction:
        # Your Bollinger Bands CCI strategy logic
        pass

    def exit_position(self, data: pd.DataFrame, position: Position) -> BrokerInstruction:
        # Your Bollinger Bands CCI strategy exit logic
        pass


class OutOfMoneyException(Exception):
    pass
