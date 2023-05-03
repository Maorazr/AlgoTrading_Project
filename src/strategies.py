from models import Strategy, BrokerInstruction, OrderType, PositionSide, Position
import random
import pdb
import pandas as pd



class BollingerRSIStrategy(Strategy):
    def __init__(self, rsi_high_mul=1.0, rsi_low_mul=1.0, stop_loss=0.07, name=""):
        self.rsi_high_mul = rsi_high_mul
        self.rsi_low_mul = rsi_low_mul
        super().__init__(name)

        self.stop_loss = stop_loss
        self.name = "BbRSI"

    def enter_position(self, data: pd.DataFrame) -> BrokerInstruction:
        last_row = data.iloc[-1]
        if last_row["Open"] < last_row["BL"] and last_row["RSI"] < (30 * self.rsi_low_mul):
            return BrokerInstruction(OrderType.OPEN_LONG, last_row["Open"])
        elif last_row["Open"] > last_row["BU"] and last_row["RSI"] > (70 * self.rsi_high_mul):
            return BrokerInstruction(OrderType.OPEN_SHORT, last_row["Open"])

    def exit_position(self, data: pd.DataFrame, position: Position) -> BrokerInstruction:
        last_row = data.iloc[-1]
        if position.side == PositionSide.LONG and last_row["TP"] >= last_row["BU"]:
            return BrokerInstruction(OrderType.CLOSE_LONG, last_row["TP"])
        elif position.side == PositionSide.SHORT and last_row["TP"] <= last_row["BL"]:
            return BrokerInstruction(OrderType.CLOSE_SHORT, last_row["TP"])

        # Stop-loss logic
        if position.side == PositionSide.LONG and position.entry_price * (1 - self.stop_loss) >= last_row["TP"]:

            return BrokerInstruction(OrderType.CLOSE_LONG, position.entry_price * (1 - self.stop_loss))  # changed to the exact stop-loss
        elif position.side == PositionSide.SHORT and position.entry_price * (1 + self.stop_loss) <= last_row["TP"]:
            return BrokerInstruction(OrderType.CLOSE_SHORT, position.entry_price * (1 + self.stop_loss))


class BollingerCCIStrategy(Strategy):
    def __init__(self, cci_high_mul=1.0, cci_low_mul=1.0, stop_loss=0.07, name="", ):
        self.cci_high_mul = cci_high_mul
        self.cci_low_mul = cci_low_mul
        super().__init__(name)
        self.stop_loss = stop_loss
        self.name = "BbCCI"

    def enter_position(self, data: pd.DataFrame) -> BrokerInstruction:
        last_row = data.iloc[-1]
        if last_row["Open"] < last_row["BL"] and last_row["CCI"] < (-100 * self.cci_low_mul):
            return BrokerInstruction(OrderType.OPEN_LONG, last_row["Open"])
        elif last_row["Open"] > last_row["BU"] and last_row["CCI"] > (100 * self.cci_high_mul):
            return BrokerInstruction(OrderType.OPEN_SHORT, last_row["Open"])

    def exit_position(self, data: pd.DataFrame, position: Position) -> BrokerInstruction:
        last_row = data.iloc[-1]

        if position.side == PositionSide.LONG and last_row["TP"] >= last_row["BU"]:
            return BrokerInstruction(OrderType.CLOSE_LONG, last_row["TP"])
        elif position.side == PositionSide.SHORT and last_row["TP"] <= last_row["BL"]:
            return BrokerInstruction(OrderType.CLOSE_SHORT, last_row["TP"])

        # Stop-loss logic
        if position.side == PositionSide.LONG and position.entry_price * (1 - self.stop_loss) >= last_row["TP"]:
            return BrokerInstruction(OrderType.CLOSE_LONG, position.entry_price * (1 - self.stop_loss))    # changed to the exact stop-loss
        elif position.side == PositionSide.SHORT and position.entry_price * (1 + self.stop_loss) <= last_row["TP"]:
            return BrokerInstruction(OrderType.CLOSE_SHORT, position.entry_price * (1 + self.stop_loss))


class BuyAndHold(Strategy):
    def __init__(self):
        self.name = "HOLD"

    def enter_position(self, data: pd.DataFrame) -> BrokerInstruction:
        # if data.index[0] == 0:
        return BrokerInstruction(OrderType.OPEN_LONG, data["Open"].iloc[-1])   # open long at the last price
        # else:
        # return None

    def exit_position(self, data: pd.DataFrame, position: Position) -> BrokerInstruction:
        return




