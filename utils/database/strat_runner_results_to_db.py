from typing import List

import jsonpickle

from backtester.models import Strategy
from utils.strategy.strategy import StrategyDetails
from utils.strategyRunner.resultsInterpretor import Results, ResultsInterpretor
from utils.strategyRunner.strategyRunner import StrategyRunner, Transaction


def update_results(strategy_id):
    strategy = Strategy.objects.get(pk=strategy_id)

    # convert the JSON string to a StrategyDetails object
    strat = StrategyDetails.fromJSON(strategy.strategyDetails)

    # run the strategy and get the transactions
    transactions: List[Transaction] = StrategyRunner.run(strat)

    # interpret the transactions and get the results
    results: Results = ResultsInterpretor.interpretResults(
        transactions, strat.capitalAllocation, strat.startDatetime)

    # convert the results to a JSON string
    strategy.results = Results.toJSON(results)

    # django method to save the changes to the database
    strategy.save()
