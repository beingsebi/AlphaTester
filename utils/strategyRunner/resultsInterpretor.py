from datetime import datetime
from typing import List
from utils.constants import TypeOfSignal
from utils.strategyRunner.strategyRunner import Transaction


class Results:
    def __init__(
        self,
        balanceOverTime: List[float] = [],
        freeFundsOverTime: List[float] = [],
        stockQuantityOverTime: List[float] = [0.0],
        timeSeries: List[datetime] = [],
        totalFees: float = 0.0,
        cntTrades: int = 0,
        totalBuySize: float = 0.0,
        totalSellSize: float = 0.0,
        cntBuys: int = 0,
        cntSells: int = 0,
        averageBuySize: float = 0.0,
        averageSellSize: float = 0.0,
        winningSellingTradesPercentage: float = 0.0,
    ):
        self.balanceOverTime = balanceOverTime
        self.freeFundsOverTime = freeFundsOverTime
        self.stockQuantityOverTime = stockQuantityOverTime
        self.timeSeries = timeSeries
        self.totalFees = totalFees
        self.cntTrades = cntTrades
        self.totalBuySize = totalBuySize  # in money
        self.totalSellSize = totalSellSize  # in money
        self.cntBuys = cntBuys
        self.cntSells = cntSells
        self.averageBuySize = averageBuySize  # in money
        self.averageSellSize = averageSellSize  # in money
        self.winningSellingTradesPercentage = (
            winningSellingTradesPercentage  # compare selling price to average buy price
        )

    def __repr__(self):
        return (
            f"Results(balanceOverTime={self.balanceOverTime},\n"
            f"freeFundsOverTime={self.freeFundsOverTime}, \n"
            f"stockQuantityOverTime={self.stockQuantityOverTime}, \n"
            f"timeSeries={self.timeSeries}, \n"
            f"totalFees={self.totalFees}, \n"
            f"cntTrades={self.cntTrades}, \n"
            f"totalBuySize={self.totalBuySize}, \n"
            f"totalSellSize={self.totalSellSize}, \n"
            f"cntBuys={self.cntBuys}, \n"
            f"cntSells={self.cntSells}, \n"
            f"averageBuySize={self.averageBuySize}, \n"
            f"averageSellSize={self.averageSellSize}, \n"
            f"winningSellingTradesPercentage={self.winningSellingTradesPercentage})"
        )


class ResultsInterpretor:
    @staticmethod
    def interpretResults(
        transactions: List[Transaction], initialBalance: float, initialTime: datetime
    ) -> Results:
        results = Results()
        freeFunds = initialBalance
        results.balanceOverTime = [initialBalance]
        results.freeFundsOverTime = [initialBalance]
        results.timeseries = [initialTime]
        stock = 0
        averageBuyPrice = 0
        winningSellTrades = 0

        for transaction in transactions:
            results.timeseries.append(
                datetime.combine(transaction.date, transaction.time)
            )
            results.cntTrades += 1
            if transaction.type == TypeOfSignal.BUY:
                print(f"buy {transaction.quantity} @ {transaction.price}")
                results.cntBuys += 1
                averageBuyPrice = averageBuyPrice * (
                    stock / (stock + transaction.quantity)
                ) + transaction.price * (
                    transaction.quantity / (stock + transaction.quantity)
                )
                stock += transaction.quantity
                freeFunds -= transaction.price * transaction.quantity + transaction.fee
                results.totalFees += transaction.fee
                results.totalBuySize += transaction.price * transaction.quantity
            else:
                print(f"sell {transaction.quantity} @ {transaction.price}")

                results.cntSells += 1
                if transaction.price > averageBuyPrice:
                    winningSellTrades += 1
                stock -= transaction.quantity
                freeFunds += transaction.price * transaction.quantity - transaction.fee
                results.totalFees += transaction.fee
                results.totalSellSize += transaction.price * transaction.quantity

            results.freeFundsOverTime.append(freeFunds)
            results.balanceOverTime.append(freeFunds + stock * transaction.price)
            results.stockQuantityOverTime.append(stock)

        results.averageBuySize = results.totalBuySize / results.cntBuys
        results.averageSellSize = results.totalSellSize / results.cntSells
        results.winningSellingTradesPercentage = winningSellTrades / results.cntSells
        return results
