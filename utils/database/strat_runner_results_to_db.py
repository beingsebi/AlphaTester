from typing import List
import jsonpickle
from backtester.models import Strategy
from utils.strategy.strategy import StrategyDetails
from utils.strategyRunner.resultsInterpretor import Results, ResultsInterpretor
from utils.strategyRunner.strategyRunner import StrategyRunner, Transaction


def update_results(strategy_id):
    strategy = Strategy.objects.get(pk=strategy_id)

    strat = StrategyDetails.fromJSON(strategy.strategyDetails)

    transactions: List[Transaction] = StrategyRunner.run(strat)

    results: Results = ResultsInterpretor.interpretResults(
        transactions, strat.capitalAllocation, strat.startDatetime
    )
    # print("-----------------------")
    # print(results)
    strategy.results = Results.toJSON(results)
    # todo might have to call json pickle here
    # strategy.description = "This is a test description"
    strategy.save()  # django method to save the changes to the database
