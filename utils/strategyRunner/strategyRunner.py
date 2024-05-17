from typing import List

from datetime import date, datetime, time, timedelta
from utils.constants import TimeframeToMinutes, TypeOfSignal
from utils.database.get_instrument_data_scripts import get_data
from utils.strategy.strategy import StrategyDetails
import traceback


class Transaction:
    def __init__(
        self,
        date: date,
        time: time,
        price: float,
        # TODO: (probably already done) metadata about the instrument , including currency
        quantity: float,
        type: TypeOfSignal,
    ):
        self.date = date
        self.time = time
        self.price = price
        self.quantity = quantity
        self.type = type

    def __str__(self) -> str:
        return f"{self.date} {self.time} {self.price} {self.quantity} {self.type.name}"

    def __repr__(self) -> str:
        return f"{self.date} {self.time} {self.price} {self.quantity} {self.type.name}"


class StrategyRunner:
    @staticmethod
    def run(strategy: StrategyDetails) -> List[Transaction]:
        transactions = []
        # WARNING: for now, the transaction will buy the close price
        # TODO: now assuming exchange fee is None
        # TODO: now assuming stopLoss and takeProfit are None
        # TODO: now assuming bidSize is fixed
        # TODO: now assuming buySignalsMode and sellSignalsMode are CNF
        # TODO: now assuming signals use open price
        # TODO: now assuming trading starts late enough to have enough data for all indicators
        # TODO: not checking if  enough money to buy
        # TODO: not checking if enough stock to sell
        # TODO: add squash transactions flag (if buy and sell at same time, then squash them into one transaction)
        # WARNING: intraday candle might actualy span multiple days

        try:
            data = get_data(  # TODO: process in batches
                strategy.instrumentName,
                strategy.startDatetime,
                strategy.endDatetime,
            )
            if not data:
                raise Exception("No data found")
        except Exception as _:
            traceback.print_exc()

        data = StrategyRunner.squashTimestamps(data, strategy.timeFrame)

        for row in data:
            print(row)
            date_time = datetime.combine(row[0], row[1])
            condition = True
            for term in strategy.buySignals:
                termCondition = False
                for signal in term:
                    if signal.operator == ">=":
                        termCondition = (
                            termCondition
                            or signal.indicator.calculateValue(date_time)
                            >= signal.threshold
                        )
                    elif signal.operator == "<=":
                        termCondition = (
                            termCondition
                            or signal.indicator.calculateValue(date_time)
                            <= signal.threshold
                        )
                    if termCondition == True:
                        break
                condition = condition and termCondition

            if condition:
                transactions.append(
                    Transaction(
                        row[0],  # date
                        row[1],  # time
                        row[5],  # close
                        strategy.bidSize.fixed,
                        TypeOfSignal.BUY,
                    )
                )

            condition = True
            for term in strategy.sellSignals:
                termCondition = False
                for signal in term:
                    if signal.operator == ">=":
                        termCondition = (
                            termCondition
                            or signal.indicator.calculateValue(date_time)
                            >= signal.threshold
                        )
                    elif signal.operator == "<=":
                        termCondition = (
                            termCondition
                            or signal.indicator.calculateValue(date_time)
                            <= signal.threshold
                        )
                    if termCondition == True:
                        break
                condition = condition and termCondition

            if condition:
                transactions.append(
                    Transaction(
                        row[0],
                        row[1],
                        row[5],
                        strategy.bidSize.fixed,
                        TypeOfSignal.SELL,
                    )
                )
        return transactions

    @staticmethod
    def squashTimestamps(data, timeframe):
        new_data = []
        index = 0
        bucket_time_start = datetime.combine(data[0][0], data[0][1])
        bucket_time_end = bucket_time_start + timedelta(
            minutes=TimeframeToMinutes[timeframe]
        )
        while index < len(data):
            date = data[index][0]
            time = data[index][1]
            open = data[index][2]
            high = data[index][3]
            low = data[index][4]
            close = data[index][5]
            spread = data[index][6]
            index += 1
            complete_candle = False
            while index < len(data):
                if datetime.combine(data[index][0], data[index][1]) >= bucket_time_end:
                    complete_candle = True
                    break
                high = max(high, data[index][3])
                low = min(low, data[index][4])
                close = data[index][5]
                spread = max(spread, data[index][6])
                index += 1
            if not complete_candle:
                break
            new_data.append((date, time, open, high, low, close, spread))
            bucket_time_start = bucket_time_end
            bucket_time_end = bucket_time_start + timedelta(
                minutes=TimeframeToMinutes[timeframe]
            )

        return new_data
