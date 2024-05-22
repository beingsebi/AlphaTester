from typing import List
from utils.constants import TypeOfSignal
from utils.strategyRunner.strategyRunner import Transaction


class resultsInterpretor:
    @staticmethod
    def interpretResults(transactions: List[Transaction], initialBalance: float):
        freeFunds = initialBalance
        investedBalance = 0
        balanceOverTime = [initialBalance]
        stock = 0
        totalFees = 0
        for transaction in transactions:
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
        return balanceOverTime, totalFees
