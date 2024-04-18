import copy
from typing import List

import jsonpickle

from .signal import Signal
from .amount import Amount


class StrategyDetails:
    def __init__(
        self,
        capitalAllocation: int,
        bidSize: Amount,
        timeFrame: str,
        takeProfit: Amount,
        stopLoss: Amount,
        exchangeFee: Amount | None,
        buySignalsMode: str,
        buySignals: List[List[Signal]],
        sellSignalsMode: str,
        sellSignals: List[List[Signal]],
    ) -> None:

        self.capitalAllocation = capitalAllocation
        # total Amount of capital allocated to the strategy

        self.bidSize = bidSize
        # dictionary with the size of the bid

        self.timeFrame = timeFrame
        # teoretic "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"
        # practic deocamdata doar "1m". Pt celelalte trebuie agregate datele

        self.takeProfit = takeProfit
        # ammount of dollars up or percentage (per trade) up

        self.stopLoss = stopLoss
        # ammount of dollars down or percentage (per trade) down

        self.exchangeFee = exchangeFee
        # no ExchangeFee (None) or Amount
        # you might want to also take into account the fee for currency conversion

        self.buySignalMode = buySignalsMode
        # "CNF" -> (a1 or a2 or..) and (b1 or...) and ..
        # "DNF" -> (a1 and a2 and..) or (b1 and...) or ..

        self.buySignals = copy.deepcopy(buySignals)  # buysignal SSSSS
        # [[Signal("indicator", 1, ">")]]

        self.sellSignalMode = sellSignalsMode
        # same as BuySignalMode

        self.sellSignals = copy.deepcopy(sellSignals)
        # same as BuySignal

    @staticmethod
    def toJSON(self):  # pylint: disable=W0211
        return jsonpickle.encode(self)

    @staticmethod
    def fromJSON(JSONstr: str):  # pylint: disable=C0103
        return jsonpickle.decode(JSONstr)

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
