import copy
from signal import Signal
from typing import List

import jsonpickle

from amount import Amount


class StrategyDetails:
    def __init__(
        self,
        CapitalAllocation: int,
        BidSize: Amount,
        TimeFrame: str,
        TakeProfit: Amount,
        StopLoss: Amount,
        ExchangeFee: Amount | None,
        BuySignalMode: str,
        BuySignal: List[List[Signal]],
        SellSignalMode: str,
        SellSignal: List[List[Signal]],
    ) -> None:

        self.CapitalAllocation = CapitalAllocation
        # total Amount of capital allocated to the strategy

        self.BidSize = BidSize
        # dictionary with the size of the bid

        self.TimeFrame = TimeFrame
        # teoretic "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"
        # practic deocamdata doar "1m". Pt celelalte trebuie agregate datele

        self.TakeProfit = TakeProfit
        # ammount of dollars up or percentage (per trade) up

        self.StopLoss = StopLoss
        # ammount of dollars down or percentage (per trade) down

        self.ExchangeFee = ExchangeFee
        # no ExchangeFee (None) or Amount
        # you might want to also take into account the fee for currency conversion

        self.BuySignalMode = BuySignalMode
        # "CNF" -> (a1 or a2 or..) and (b1 or...) and ..
        # "DNF" -> (a1 and a2 and..) or (b1 and...) or ..

        self.BuySignal = copy.deepcopy(BuySignal)
        # [[Signal("indicator", 1, ">")]]

        self.SellSignalMode = SellSignalMode
        # same as BuySignalMode

        self.SellSignal = copy.deepcopy(SellSignal)
        # same as BuySignal

    def toJSON(self):
        return jsonpickle.encode(self)

    @staticmethod
    def fromJSON(JSONstr: str):
        return jsonpickle.decode(JSONstr)

    def dummy_print(self):
        print("CapitalAllocation: ", self.CapitalAllocation)


# example
a = StrategyDetails(
    200,
    Amount(5, None),
    "1m",
    Amount(1, None),
    Amount(1, None),
    Amount(0.1, None),
    "CNF",
    [[Signal("indicator", 1, ">")]],
    "DNF",
    [[Signal("indicator", 1, ">")]],
)

json = a.toJSON()
print(json + "\n\n")
b: StrategyDetails = StrategyDetails.fromJSON(json)

b.dummy_print()
