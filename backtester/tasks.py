from time import sleep
from backtester.models import Strategy
from celery import shared_task
from utils.database.strat_runner_results_to_db import update_results


@shared_task()
def expensive_task(strategy_id):
    print("recieved", strategy_id)
    update_results(strategy_id)
    # sleep(5)  # Simulate expensive operation(s) that freeze Django
    print("done", strategy_id)
