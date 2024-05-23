from datetime import datetime
from typing import List
from utils.constants import TypeOfSignal
from utils.strategyRunner.strategyRunner import Transaction


class Results:
    def __init__(
        self, balanceOverTime: List[float], totalFees: float, timeSeries: List[datetime]
    ):
        self.balanceOverTime = balanceOverTime
        self.totalFees = totalFees
        self.timeSeries = timeSeries

    def __repr__(self):
        return (
            f"Results(\nbalanceOverTime={self.balanceOverTime},\n"
            f"totalFees={self.totalFees},\n"
            f"timeSeries={self.timeSeries}\n"
            ")"
        )


class ResultsInterpretor:
    @staticmethod
    def interpretResults(
        transactions: List[Transaction], initialBalance: float, initialTime: datetime
    ) -> Results:
        freeFunds = initialBalance
        investedBalance = 0
        balanceOverTime = [initialBalance]
        timeseries = [initialTime]
        stock = 0
        totalFees = 0
        for transaction in transactions:
            timeseries.append(datetime.combine(transaction.date, transaction.time))
            if transaction.type == TypeOfSignal.BUY:
                stock += transaction.quantity
                freeFunds -= transaction.price * transaction.quantity + transaction.fee
                totalFees += transaction.fee
                investedBalance += transaction.price * transaction.quantity
            else:
                stock -= transaction.quantity
                freeFunds += transaction.price * transaction.quantity - transaction.fee
                totalFees += transaction.fee
                investedBalance -= transaction.price * transaction.quantity

            balanceOverTime.append(freeFunds + stock * transaction.price)
        return Results(balanceOverTime, totalFees, timeseries)
