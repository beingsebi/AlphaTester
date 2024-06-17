import logging
from datetime import datetime
from typing import List

import jsonpickle

from utils.constants import TypeOfSignal
from utils.strategyRunner.strategyRunner import Transaction

logger = logging.getLogger(__name__)


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
        profit: float = 0.0,
        maxWinningStreak: int = 0,
        maxLosingStreak: int = 0,
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
        self.winningSellingTradesPercentage = winningSellingTradesPercentage  # compare selling price to average buy price
        self.profit = profit  # in money
        self.maxWinningStreak = maxWinningStreak
        self.maxLosingStreak = maxLosingStreak

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
            f"winningSellingTradesPercentage={self.winningSellingTradesPercentage}) \n"
            f"profit={self.profit})")

    @staticmethod
    def toJSON(self):
        return jsonpickle.encode(self)

    @staticmethod
    def fromJSON(JSONstr: str):
        return jsonpickle.decode(JSONstr)


class ResultsInterpretor:

    @staticmethod
    def interpretResults(transactions: List[Transaction], initialBalance: float,
                         initialTime: datetime) -> Results:
        results = Results()
        freeFunds = initialBalance
        results.balanceOverTime = [initialBalance]
        results.freeFundsOverTime = [initialBalance]
        results.timeSeries = [initialTime]
        stock = 0
        averageBuyPrice = 0
        winningSellTrades = 0
        winningStreak = 0
        losingStreak = 0

        for transaction in transactions:
            results.timeSeries.append(
                datetime.combine(transaction.date, transaction.time))
            results.cntTrades += 1
            if transaction.type == TypeOfSignal.BUY:
                logger.debug(
                    f"buy {transaction.quantity} @ {transaction.price}")
                results.cntBuys += 1
                averageBuyPrice = averageBuyPrice * (
                    stock /
                    (stock + transaction.quantity)) + transaction.price * (
                        transaction.quantity / (stock + transaction.quantity))
                stock += transaction.quantity
                freeFunds -= transaction.price * transaction.quantity + transaction.fee
                results.totalFees += transaction.fee
                results.totalBuySize += transaction.price * transaction.quantity
            else:
                logger.debug(
                    f"sell {transaction.quantity} @ {transaction.price}")

                results.cntSells += 1
                if transaction.price > averageBuyPrice:
                    winningSellTrades += 1
                    losingStreak = 0
                    winningStreak += 1
                    if winningStreak > results.maxWinningStreak:
                        results.maxWinningStreak = winningStreak
                elif transaction.price < averageBuyPrice:
                    losingStreak += 1
                    winningStreak = 0
                    if losingStreak > results.maxLosingStreak:
                        results.maxLosingStreak = losingStreak
                else:
                    winningStreak = 0
                    losingStreak = 0

                stock -= transaction.quantity
                freeFunds += transaction.price * transaction.quantity - transaction.fee
                results.totalFees += transaction.fee
                results.totalSellSize += transaction.price * transaction.quantity

            results.freeFundsOverTime.append(freeFunds)
            results.balanceOverTime.append(freeFunds +
                                           stock * transaction.price)
            results.stockQuantityOverTime.append(stock)

        if results.cntBuys != 0:
            results.averageBuySize = results.totalBuySize / results.cntBuys
        else:
            results.averageBuySize = 0

        if results.cntSells != 0:
            results.averageSellSize = results.totalSellSize / results.cntSells
        else:
            results.averageSellSize = 0

        if results.cntSells != 0:
            results.winningSellingTradesPercentage = (winningSellTrades /
                                                      results.cntSells)
        else:
            results.winningSellingTradesPercentage = 0

        if len(results.balanceOverTime) > 0:
            results.profit = results.balanceOverTime[-1] - initialBalance
        else:
            results.profit = 0

        return results
