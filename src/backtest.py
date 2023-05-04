from typing import Dict
import pdb

from models import (
    OutOfMoneyException,
    Strategy,
    BrokerInstruction,
    OrderType,
    PositionSide,
    Position,
)
import pandas as pd
from models import BollingerBandsRSI, BollingerBandsCCI
from summary import Summary
from utils import adjust_types


class Backtest:
    def __init__(
        self,
        data: pd.DataFrame,
        commission: float,
        balance: int,
        strategy: Strategy,
        leverage: int = 1.0,
        window_size: int = 20,
        buy_percentage: float = 0.05,
    ):
        self.data = data
        self.commission = commission
        self.balance = balance
        self.strategy = strategy
        self.leverage = leverage
        self.window_size = window_size
        self.buy_percentage = buy_percentage


    def broker_action(self, qty: float, price: float, instruction: BrokerInstruction):
        if instruction.order_type == OrderType.OPEN_LONG:
            self.balance -= qty * price * (1 + self.commission)
            return Position(qty, price, PositionSide.LONG)

        elif instruction.order_type == OrderType.OPEN_SHORT:
            self.balance += qty * price * (1 - self.commission)
            return Position(qty, price, PositionSide.SHORT)

        elif instruction.order_type == OrderType.CLOSE_LONG:
            self.balance += qty * price * (1 - self.commission)
            return None
            
        else:  # OrderType.CLOSE_SHORT
            self.balance -= qty * price * (1 + self.commission)
            return None


    def calc_price(
        self, instructions: BrokerInstruction, candle: Dict, change_size: int = 2.0
    ):
        curr_close = candle["TP"]
        curr_open = candle["Open"]

        slippage_rate = ((curr_close - curr_open) / curr_open) / change_size

        price = instructions.price

        if instructions.order_type in [OrderType.OPEN_LONG, OrderType.CLOSE_SHORT]:
            return max(price + price * slippage_rate, price)

        else:
            return min(price - price * slippage_rate, price)

    def calc_return(self, position: Position, close_price: float):
        open_price = position.entry_price

        if position.side == PositionSide.SHORT:
            return_rate = (open_price - close_price) / open_price
        else:
            return_rate = (close_price - open_price) / open_price

        return_rate_with_comm = return_rate * (1 - self.commission) * self.leverage
        return return_rate_with_comm


    def backtest(self):
        
        position: Position = None
        data = self.data.copy(deep=True)
        data['Pos'] = 0
        data['Strategy'] = self.strategy.name
        for i in range(self.window_size, len(self.data) + 1):
            curr_data = data[i - self.window_size : i]
            past_data = curr_data[:-1]
            curr_row_idx = data.index[i - 1]
            curr_candle = curr_data[-1:].to_dict(orient="records")[0]

            data.loc[curr_row_idx, "Balance"] = self.balance

            if position is None:
                data.loc[curr_row_idx, "Pos"] = curr_candle["Open"]
                instruction: BrokerInstruction = self.strategy.enter_position(
                    data=past_data
                )
                
                if instruction is not None:
                    data.loc[curr_row_idx, "Actions"] = instruction.order_type
                    
                    actual_price = self.calc_price(instruction, curr_candle)
                    qty = (
                        self.balance * self.buy_percentage / actual_price  
                    ) * self.leverage
                    qty = round(qty)
                    position = self.broker_action(qty, actual_price, instruction)
                    if instruction.order_type in [OrderType.OPEN_LONG, OrderType.OPEN_SHORT]:
                        data.loc[curr_row_idx, 'Pos'] = position.qty
                   
            else:
                if i == len(self.data):
                    last_close = list(curr_data["TP"])[-1]
                    if position.side == PositionSide.LONG:
                        instruction = BrokerInstruction(
                            OrderType.CLOSE_LONG, last_close
                        )
                    else:
                        instruction = BrokerInstruction(
                            OrderType.CLOSE_SHORT, last_close
                        )
                else:
                    instruction = self.strategy.exit_position(
                        data=past_data, position=position
                    )

                if instruction is not None:
                    data.loc[curr_row_idx, "Actions"] = 0  # position closed
                    
                    actual_price = self.calc_price(instruction, curr_candle)
                    return_rate = self.calc_return(position, actual_price)

                    data.loc[curr_row_idx, "Return rate"] = return_rate
                    position = self.broker_action(
                        position.qty, actual_price, instruction
                    )
                    if instruction.order_type in [OrderType.CLOSE_LONG, OrderType.CLOSE_SHORT]:
                        data.loc[curr_row_idx, 'Pos'] = 0
                        data.loc[curr_row_idx, "Balance"] = self.balance
        
        trading_data = data[self.window_size -1:]
        trading_data.to_csv(f"../results/stra_tick_res/{self.strategy.name}_{trading_data.iloc[1]['Ticker']}.csv")
        return trading_data

