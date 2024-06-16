import copy
from datetime import datetime
from typing import List

import jsonpickle

from utils.constants import SignalsChoicesMode, Timeframe
from utils.strategy.indicators.baseIndicator import BaseIndicator

from .amount import Amount
from .signal import Signal


class StrategyDetails:

    def __init__(
        self,
        instrumentName: str,  # has to be the same as the one in the database 
        # | TODO: (nice to have) dynamic enum or something similar
        capitalAllocation:
        float,  # using the currency in which the instrument is traded
        timeFrame: Timeframe,
        buySize: Amount,  # this is with respect to money, not to stocks
        sellSize: Amount,  # this is with respect to money, not to stocks
        takeProfit: Amount | None,
        stopLoss: Amount | None,
        indicators: List[BaseIndicator],
        buySignalsMode: SignalsChoicesMode,
        buySignals: List[List[Signal]],
        sellSignalsMode: SignalsChoicesMode,
        sellSignals: List[List[Signal]],
        exchangeBuyFee: Amount | None = None,
        exchangeSellFee: Amount | None = None,
        startDatetime: datetime | None = None,
        endDatetime: datetime | None = None,
    ) -> None:
        self.instrumentName = instrumentName
        # has to be the same as the one in the database

        self.capitalAllocation = capitalAllocation
        # total Amount of capital allocated to the strategy

        self.timeFrame = timeFrame
        # timeFrame of the candles used in the strategy

        self.buySize = buySize
        # Amount of one buy trade

        self.sellSize = sellSize
        # Amount of one sell trade

        # will keep the medium price of the shares bought and will compare with respect to it. not taking into account fees
        self.takeProfit = takeProfit
        # with respect to the ammount traded at one particular time. liquidates all positions

        self.stopLoss = stopLoss
        # with respect to the ammount traded at one particular time. liquidates all positions

        self.indicators = copy.deepcopy(indicators)
        # instances of the indicators used in the strategy with their parameters

        self.buySignalMode = buySignalsMode
        # "CNF" -> (a1 or a2 or..) and (b1 or...) and ..
        # "DNF" -> (a1 and a2 and..) or (b1 and...) or ..

        self.buySignals = copy.deepcopy(buySignals)
        # [[Signal("indicator", thresh, ">=")]]

        self.sellSignalMode = sellSignalsMode
        # same as BuySignalMode

        self.sellSignals = copy.deepcopy(sellSignals)
        # same as BuySignals

        self.exchangeBuyFee = exchangeBuyFee
        # no exchangeBuyFee (None) or Amount
        # you might want to also take into account the fee for currency conversion

        self.exchangeSellFee = exchangeSellFee
        # no exchangeSellFee (None) or Amount
        # you might want to also take into account the fee for currency conversion

        self.startDatetime = startDatetime
        # date and time from which the strategy will start trading
        # if none => start trading from the first available date

        self.endDatetime = endDatetime
        # date and time from which the strategy will stop trading
        # if none => stop trading at the last available date

    @staticmethod
    def toJSON(self):  # pylint: disable=W0211
        return jsonpickle.encode(self)

    @staticmethod
    def fromJSON(JSONstr: str):  # pylint: disable=C0103
        return jsonpickle.decode(JSONstr)

    def __str__(self) -> str:
        return (f"Strategy Details:\n"
                f"instrumentName: {self.instrumentName}\n"
                f"capitalAllocation: {self.capitalAllocation}\n"
                f"timeFrame: {self.timeFrame}\n"
                f"buySize: {self.buySize}\n"
                f"sellSize: {self.sellSize}\n"
                f"takeProfit: {self.takeProfit}\n"
                f"stopLoss: {self.stopLoss}\n"
                f"indicators: {self.indicators}\n"
                f"buySignalMode: {self.buySignalMode}\n"
                f"buySignals: {self.buySignals}\n"
                f"sellSignalMode: {self.sellSignalMode}\n"
                f"sellSignals: {self.sellSignals}\n"
                f"exchangeFee: {self.exchangeBuyFee}\n"
                f"exchangeFee: {self.exchangeSellFee}\n"
                f"startDatetime: {self.startDatetime}\n"
                f"endDatetime: {self.endDatetime}\n")

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
