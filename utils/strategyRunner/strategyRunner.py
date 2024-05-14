from typing import List

from datetime import date, time
from utils.constants import TypeOfSignal
from utils.strategy.strategy import StrategyDetails


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


class StrategyRunner:
    @staticmethod
    def run(strategy: StrategyDetails) -> List[Transaction]:
        transactions = []
