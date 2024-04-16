import copy
from signal import signal
from typing import List

import jsonpickle

from amount import amount


class strategy:
    def __init__(
        self,
        CapitalAllocation: int,
        BidSize: amount,
        TimeFrame: str,
        TakeProfit: amount,
        StopLoss: amount,
        ExchangeFee: amount,
        BuySignalMode: str,
        BuySignal: List[List[signal]],
        SellSignalMode: str,
        SellSignal: List[List[signal]],
    ) -> None:

        self.CapitalAllocation = CapitalAllocation
        # total amount of capital allocated to the strategy

        self.BidSize = BidSize
        # dictionary with the size of the bid

        self.TimeFrame = TimeFrame
        # teoretic "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"
        # practic deocamdata doar "1m". Pt celelalte trebuie agregate datele

        self.TakeProfit = TakeProfit
        # ammount of dollars up or percentage (per trade) up

        self.StopLoss = StopLoss
        # ammount of dollars down or percentage (per trade) down

        self.ExchangeFee = ExchangeFee  # you might want to also take into account the fee for currency conversion
        # None (free) or {"fixed" : 0.1, "percentage" : None} or {"fixed" : None, "percentage" : 0.1}

        self.BuySignalMode = BuySignalMode
        # "CNF" -> (a1 or a2 or..) and (b1 or...) and ..
        # "DNF" -> (a1 and a2 and..) or (b1 and...) or ..

        self.BuySignal = copy.deepcopy(BuySignal)
        # [[signal("indicator", 1, ">")]]

        self.SellSignalMode = SellSignalMode
        # same as BuySignalMode

        self.SellSignal = copy.deepcopy(SellSignal)
        # same as BuySignal

    def toJSON(self):
        return jsonpickle.encode(self)

    @staticmethod
    def fromJSON(JSONstr: str):
        return jsonpickle.decode(JSONstr)

    # def dummy_print(self):
    #     print("CapitalAllocation: ", self.CapitalAllocation)


# example
# a = strategy(
#     200,
#     amount(5, None),
#     "1m",
#     amount(1, None),
#     amount(1, None),
#     amount(0.1, None),
#     "CNF",
#     [[signal("indicator", 1, ">")]],
#     "DNF",
#     [[signal("indicator", 1, ">")]],
# )

# json = a.toJSON()
# print(json + "\n\n")
# b: strategy = strategy.fromJSON(json)

# b.dummy_print()
