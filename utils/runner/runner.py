from typing import List

import sqlalchemy
from utils.constants import TypeOfSignal
from utils.strategy.strategy import StrategyDetails


class Transaction:
    def __init__(
        self,
        date: sqlalchemy.types.Date,
        time: sqlalchemy.types.Time,
        price: float,
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
