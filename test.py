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

from utils.strategyRunner.strategyRunner import StrategyRunner


def test_strat():
    my_sma = IndicatorFactory.createIndicator(
        "ZXAUUSD",
        constants.IndicatorNames.SMA,
        constants.Timeframe.H1,
        length=5,
        source=constants.Sources.CLOSE,
    )

    strategy = StrategyDetails(
        "ZXAUUSD",
        1000,
        constants.Timeframe.M1,
        Amount(10),
        Amount(5),
        None,
        None,
        [my_sma],
        constants.SignalsChoicesMode.CNF,
        [[Signal(my_sma, 100, ">=")]],
        constants.SignalsChoicesMode.CNF,
        [[Signal(my_sma, 100, "<=")]],
        None,
        None,
        datetime(2024, 1, 3, 9, 30, 0),
        datetime(2024, 1, 3, 9, 35, 0),
    )

    print(strategy)

    r = StrategyRunner.run(strategy)
    if r:
        for i in r:
            print(i)


test_strat()


def test_get_data():
    data = get_data(
        "ZXAUUSD",
        datetime(2024, 1, 2, 1, 0, 0),
        datetime(2024, 1, 2, 1, 10, 0),
    )

    for i in data:
        print(i)
