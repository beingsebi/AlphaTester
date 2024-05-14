from utils.strategy.amount import Amount
from utils.strategy.indicators.indicatorFactory import IndicatorFactory
from utils.strategy.indicators.sma import SMA
from utils import constants
from utils import database as mdb
from utils.strategy.strategy import StrategyDetails
from utils.strategy.signal import Signal

# sme = SMA(constants.IndicatorNames.EMA, constants.Timeframe.D1,
#           length=20, source=constants.Sources.CLOSE)

# print(sme.name.name)

# mdb.insert_data_into_table("ZXAUUSD_2024_01.csv")


# class StrategyDetails:
#     def __init__(
#         self,
#         instrumentName: str,  # has to be the same as the one in the database
#         capitalAllocation: int,  # the currency in which the instrument is traded
#         timeFrame: Timeframe,
#         bidSize: Amount,
#         takeProfit: Amount | None,
#         stopLoss: Amount | None,
#         indicators: List[BaseIndicator],
#         buySignalsMode: SignalsChoicesMode,
#         buySignals: List[List[Signal]],
#         sellSignalsMode: SignalsChoicesMode,
#         sellSignals: List[List[Signal]],
#         exchangeFee: Amount | None = None,
#         start_date: datetime | None = None,
#         end_date: datetime | None = None,
#     ) -> None:


my_sma = IndicatorFactory.createIndicator(
    "ZXAUUSD", constants.IndicatorNames.SMA, constants.Timeframe.M1, length=20, source=constants.Sources.CLOSE)

strategy = StrategyDetails(
    "ZXAUUSD",
    1000,
    constants.Timeframe.M1,
    Amount(10),
    None,
    None,
    [my_sma],
    constants.SignalsChoicesMode.CNF,
    [[Signal(my_sma, 10, ">=")]],
    constants.SignalsChoicesMode.CNF,
    [[Signal(my_sma, 10, "<=")]],
)

print(strategy)
