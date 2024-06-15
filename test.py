import django

django.setup()
import pickle
from datetime import datetime

from django.conf import settings

from backtester.models import Strategy
from utils import constants, strategy
from utils.database import populate_database_scripts as mdb
from utils.database import strat_runner_results_to_db
from utils.database.get_instrument_data_scripts import get_data
from utils.strategy.amount import Amount
from utils.strategy.indicators.indicatorFactory import IndicatorFactory
from utils.strategy.indicators.sma import SMA
from utils.strategy.signal import Signal
from utils.strategy.strategy import StrategyDetails
from utils.strategyRunner.resultsInterpretor import Results, ResultsInterpretor
from utils.strategyRunner.strategyRunner import StrategyRunner

# mdb.insert_data_into_table("ZXAUUSD_2024_01.csv")


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
        [[Signal(my_sma, 2045.15, "<=")]],
        constants.SignalsChoicesMode.CNF,  # sell signals mode
        [[Signal(my_sma, 2045.16, ">=")]],
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
    print("------------------------")
    proc: Results = ResultsInterpretor.interpretResults(
        r, strategy.capitalAllocation, strategy.startDatetime)
    print(proc)
    plott(proc)


# print(my_ema)
# aux = my_ema.calculateValue(datetime(2024, 1, 3, 9, 30, 0))
# print(aux)


def test_get_data():
    data = get_data(
        "ZXAUUSD",
        datetime(2024, 1, 2, 1, 0, 0),
        datetime(2024, 1, 2, 1, 10, 0),
    )

    for i in data:
        print(i)


# test_strat()

# def test_runn():

#     strt = Strategy.objects.get(id=1)
#     # strt.strategyDetails = StrategyDetails.fromJSON(strt.strategyDetails)
#     # print(strt.strategyDetails)
#     strat_runner_results_to_db.update_results(strt)

# test_runn()
