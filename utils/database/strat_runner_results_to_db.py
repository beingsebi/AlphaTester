from typing import List
from backtester.models import Strategy
from utils.strategyRunner.resultsInterpretor import Results, ResultsInterpretor
from utils.strategyRunner.strategyRunner import StrategyRunner, Transaction


def update_results(strategy: Strategy):
    transactions: List[Transaction] = StrategyRunner.run(strategy.strategyDetails)
    results: Results = ResultsInterpretor.interpretResults(
        transactions, strategy.initial_balance, strategy.start_datetime
    )
    # print(results)
    strategy.results = results
    # todo might have to call json pickle here
    # strategy.description = "This is a test description"
    strategy.save()  # django method to save the changes to the database
