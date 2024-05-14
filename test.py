from utils.strategy.amount import Amount
from utils.strategy.indicators.indicatorFactory import IndicatorFactory
from utils.strategy.indicators.sma import SMA
from utils import constants
from utils.database import populate_database_scripts as mdb
from utils.strategy.strategy import StrategyDetails
from utils.strategy.signal import Signal

# sme = SMA(constants.IndicatorNames.EMA, constants.Timeframe.D1,
#           length=20, source=constants.Sources.CLOSE)

# print(sme.name.name)

# mdb.insert_data_into_table("ZXAUUSD_2024_01.csv")

# my_sma = IndicatorFactory.createIndicator(
#     "ZXAUUSD", constants.IndicatorNames.SMA, constants.Timeframe.M1, length=20, source=constants.Sources.CLOSE)

# strategy = StrategyDetails(
#     "ZXAUUSD",
#     1000,
#     constants.Timeframe.M1,
#     Amount(10),
#     None,
#     None,
#     [my_sma],
#     constants.SignalsChoicesMode.CNF,
#     [[Signal(my_sma, 10, ">=")]],
#     constants.SignalsChoicesMode.CNF,
#     [[Signal(my_sma, 10, "<=")]],
# )

# print(strategy)

from utils.database.get_instrument_data_scripts import get_data
from utils.database.get_instrument_data_scripts import get_data
from datetime import date, time


data = get_data(
    "ZXAUUSD",
    date(2024, 1, 2),
    time(1, 0, 0),
    date(2024, 1, 2),
    time(1, 10, 0),
)

for i in data:
    print(i)
