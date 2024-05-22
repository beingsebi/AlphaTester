from utils.strategy.amount import Amount
from utils.strategy.indicators.indicatorFactory import IndicatorFactory
from utils.strategy.indicators.sma import SMA
from utils import constants
from utils.database import populate_database_scripts as mdb
from utils.strategy.strategy import StrategyDetails
from utils.strategy.signal import Signal
from utils.database.get_instrument_data_scripts import get_data
from utils.database.get_instrument_data_scripts import get_data
from datetime import datetime

from utils.strategyRunner.resultsInterpretor import resultsInterpretor
from utils.strategyRunner.strategyRunner import StrategyRunner


def test_strat():
    my_sma = IndicatorFactory.createIndicator(
        "ZXAUUSD",
        constants.IndicatorNames.SMA,
        constants.Timeframe.H1,
        length=5,
        source=constants.Sources.CLOSE,
    )

    my_ema = IndicatorFactory.createIndicator(
        "ZXAUUSD",
        constants.IndicatorNames.EMA,
        constants.Timeframe.H1,
        length=7,
        source=constants.Sources.CLOSE,
    )

    strategy = StrategyDetails(
        "ZXAUUSD",
        10000,
        constants.Timeframe.M30,
        Amount(1000),
        Amount(1000),
        None,
        None,
        [my_sma, my_ema],
        constants.SignalsChoicesMode.CNF,
        [[Signal(my_ema, 2045.15, "<=")]],
        constants.SignalsChoicesMode.CNF,
        [[Signal(my_ema, 2045.16, ">=")]],
        None,
        None,
        datetime(2024, 1, 4, 8, 31, 0),
        datetime(2024, 1, 4, 14, 35, 0),
    )

    r = StrategyRunner.run(strategy)
    if r:
        for i in r:
            print(i)
    proc = resultsInterpretor.interpretResults(r, strategy.capitalAllocation)
    print(proc[0])
    print(proc[1])


# print(my_ema)
# aux = my_ema.calculateValue(datetime(2024, 1, 3, 9, 30, 0))
# print(aux)
test_strat()


def test_get_data():
    data = get_data(
        "ZXAUUSD",
        datetime(2024, 1, 2, 1, 0, 0),
        datetime(2024, 1, 2, 1, 10, 0),
    )

    for i in data:
        print(i)
