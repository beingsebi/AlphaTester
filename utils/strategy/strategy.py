import copy
from typing import List
from datetime import datetime
import jsonpickle

from utils.constants import SignalsChoicesMode, Timeframe
from utils.strategy.indicators.baseIndicator import BaseIndicator

from .signal import Signal
from .amount import Amount


class StrategyDetails:
    def __init__(
        self,
        instrumentName: str,  # has to be the same as the one in the database TODO: enum
        capitalAllocation: int,  # the currency in which the instrument is traded
        timeFrame: Timeframe,
        bidSize: Amount,
        takeProfit: Amount | None,
        stopLoss: Amount | None,
        indicators: List[BaseIndicator],
        buySignalsMode: SignalsChoicesMode,
        buySignals: List[List[Signal]],
        sellSignalsMode: SignalsChoicesMode,
        sellSignals: List[List[Signal]],
        exchangeFee: Amount | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> None:
        self.instrumentName = instrumentName
        # has to be the same as the one in the database

        self.capitalAllocation = capitalAllocation
        # total Amount of capital allocated to the strategy

        self.timeFrame = timeFrame
        # teoretic "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"
        # practic deocamdata doar "1m". Pt celelalte trebuie agregate datele

        self.bidSize = bidSize
        # dictionary with the size of the bid

        self.takeProfit = takeProfit
        # with respect to the ammount traded at one particular time. liquidates all positions

        self.stopLoss = stopLoss
        # with respect to the ammount traded at one particular time. liquidates all positions

        self.indicators = copy.deepcopy(indicators)
        # instances of the indicators used in the strategy with their parameters

        self.buySignalMode = buySignalsMode
        # "CNF" -> (a1 or a2 or..) and (b1 or...) and ..
        # "DNF" -> (a1 and a2 and..) or (b1 and...) or ..

        self.buySignals = copy.deepcopy(buySignals)  # buysignal SSSSS
        # [[Signal("indicator", 1, ">")]]

        self.sellSignalMode = sellSignalsMode
        # same as BuySignalMode

        self.sellSignals = copy.deepcopy(sellSignals)
        # same as BuySignal

        self.exchangeFee = exchangeFee
        # no ExchangeFee (None) or Amount
        # you might want to also take into account the fee for currency conversion

        self.start_date = start_date
        # date from which the strategy will start trading
        # if none => start trading from the first available date

        self.end_date = end_date
        # date from which the strategy will stop trading
        # if none => stop trading at the last available date

    @staticmethod
    def toJSON(self):  # pylint: disable=W0211
        return jsonpickle.encode(self)

    @staticmethod
    def fromJSON(JSONstr: str):  # pylint: disable=C0103
        return jsonpickle.decode(JSONstr)

    def __str__(self) -> str:
        return (
            f"Strategy Details:\n"
            f"instrumentName: {self.instrumentName}\n"
            f"capitalAllocation: {self.capitalAllocation}\n"
            f"timeFrame: {self.timeFrame}\n"
            f"bidSize: {self.bidSize}\n"
            f"takeProfit: {self.takeProfit}\n"
            f"stopLoss: {self.stopLoss}\n"
            f"indicators: {self.indicators}\n"
            f"buySignalMode: {self.buySignalMode}\n"
            f"buySignals: {self.buySignals}\n"
            f"sellSignalMode: {self.sellSignalMode}\n"
            f"sellSignals: {self.sellSignals}\n"
            f"exchangeFee: {self.exchangeFee}\n"
            f"start_date: {self.start_date}\n"
            f"end_date: {self.end_date}"

        )

    def dummyPrint(self):
        print("CapitalAllocation: ", self.capitalAllocation)


# example
# a = StrategyDetails(
#     200,
#     Amount(5, None),
#     "1m",
#     Amount(1, None),
#     Amount(1, None),
#     Amount(0.1, None),
#     "CNF",
#     [[Signal("indicator", 1, ">")]],
#     "DNF",
#     [[Signal("indicator", 1, ">")]],
# )

# json_default = StrategyDetails.toJSON(a)
# print(json_default + "\n\n")
# b: StrategyDetails = StrategyDetails.fromJSON(json)

# b.dummy_print()
