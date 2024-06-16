from typing import List

import jsonpickle

from backtester.models import Strategy
from utils.strategy.strategy import StrategyDetails
from utils.strategyRunner.resultsInterpretor import Results, ResultsInterpretor
from utils.strategyRunner.strategyRunner import StrategyRunner, Transaction


def update_results(strategy_id):
    strategy = Strategy.objects.get(pk=strategy_id)

    strat = StrategyDetails.fromJSON(
        strategy.strategyDetails
    )  # convert the JSON string to a StrategyDetails object

    transactions: List[Transaction] = StrategyRunner.run(
        strat)  # run the strategy and get the transactions

    results: Results = ResultsInterpretor.interpretResults(
        transactions, strat.capitalAllocation,
        strat.startDatetime)  # interpret the transactions and get the results

    strategy.results = Results.toJSON(
        results)  # convert the results to a JSON string

    strategy.save()  # django method to save the changes to the database
