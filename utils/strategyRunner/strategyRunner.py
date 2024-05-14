from typing import List

from datetime import date, datetime, time
from utils.constants import TypeOfSignal
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
        amount: float,
        type: TypeOfSignal,
    ):
        self.date = date
        self.time = time
        self.price = price
        self.amount = amount
        self.type = type

    def __str__(self) -> str:
        return f"{self.date} {self.time} {self.price} {self.amount} {self.type.name}"

    def __repr__(self) -> str:
        return f"{self.date} {self.time} {self.price} {self.amount} {self.type.name}"


class StrategyRunner:
    @staticmethod
    def run(strategy: StrategyDetails) -> List[Transaction]:
        transactions = []
        # TODO: now assuming timeFrame is 1 minute
        # TODO: now assuming exchange fee is None
        # TODO: now assuming startDatetime and endDatetime are not None
        # TODO: now assuming stopLoss and takeProfit are None
        # TODO: now assuming bidSize is fixed
        # TODO: now assuming buySignalsMode and sellSignalsMode are CNF
        # TODO: now assuming signals use open price
        # TODO: not checking if enough money to buy
        # TODO: not checking if enough stock to sell

        try:
            data = get_data(  # TODO: process in batches
                strategy.instrumentName,
                strategy.startDatetime,
                strategy.endDatetime,
            )
            if not data:
                raise Exception("No data found")

            for row in data:
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

        except Exception as _:
            traceback.print_exc()
