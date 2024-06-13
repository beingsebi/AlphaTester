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

from utils.strategyRunner.resultsInterpretor import Results, ResultsInterpretor
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
        10000,  # capital allocation
        constants.Timeframe.M30,
        Amount(1500),  # buy size
        Amount(100),  # sell size
        None,  # take profit
        None,  #   stop loss
        [my_sma, my_ema],
        constants.SignalsChoicesMode.CNF,  # buy signals mode
        [[Signal(my_ema, 2045.15, "<=")]],
        constants.SignalsChoicesMode.CNF,  # sell signals mode
        [[Signal(my_ema, 2045.16, ">=")]],
        Amount(0.12),  # buy fee
        Amount(0.1),  # sell fee
        datetime(2024, 1, 4, 8, 31, 0),  # start datetime
        datetime(2024, 1, 5, 14, 35, 0),  # end datetime
    )

    r = StrategyRunner.run(strategy)
    if r:
        for i in r:
            print(i)
    print(strategy.startDatetime)
    proc: Results = ResultsInterpretor.interpretResults(
        r, strategy.capitalAllocation, strategy.startDatetime
    )
    plott(proc)


def plott(proc: Results):
    import matplotlib.pyplot as plt

    timeseries = proc.timeSeries
    balance = proc.balanceOverTime
    # print(balance)
    fig, ax = plt.subplots()
    ax.plot(timeseries, balance)
    ax.set_xlabel("Time")
    ax.set_ylabel("Balance")
    ax.set_title("Balance Over Time")
    ax.set_ylim(min(balance) - 5, max(balance) + 5)  # Adjust y-axis limits
    fig.autofmt_xdate()
    plt.show()  # TODO SAVE the plot


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
