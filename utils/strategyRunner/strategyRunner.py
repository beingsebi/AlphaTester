from typing import List

from datetime import date, datetime, time, timedelta
from utils.constants import Timeframe, TimeframeToMinutes, TypeOfSignal
from utils.database.get_instrument_data_scripts import get_data
from utils.strategy.amount import Amount
from utils.strategy.signal import Signal
from utils.strategy.strategy import StrategyDetails
import traceback


class Transaction:
    def __init__(
        self,
        date: date,
        time: time,
        price: float,
        quantity: float,
        type: TypeOfSignal,
        fee: float,
    ):
        self.date = date
        self.time = time
        self.price = price
        self.quantity = quantity
        self.type = type
        self.fee = fee

    def __str__(self) -> str:
        return f"{self.date} {self.time} {self.price} {self.quantity} {self.type.name}"

    def __repr__(self) -> str:
        return f"{self.date} {self.time} {self.price} {self.quantity} {self.type.name}"


class StrategyRunner:
    @staticmethod
    def run(strategy: StrategyDetails) -> List[Transaction]:
        transactions = []
        # TODO: now assuming stopLoss and takeProfit are None
        # TODO: now assuming signals use open price ??? idk is this has to be solved here or in the signal class. same for indicators
        # TODO IMPORTANT: now assuming trading starts late enough to have enough data for all indicators
        # TODO: add squash transactions flag (if buy and sell at same time, then squash them into one transaction)
        # WARNING: for now, the transaction will buy the close price
        # WARNING: intraday candle might actualy span multiple days

        try:
            data = get_data(  # TODO: process in batches
                strategy.instrumentName,
                strategy.startDatetime,
                strategy.endDatetime,
            )
            if not data:
                raise Exception("No data found")
        except Exception as _:
            traceback.print_exc()

        data = StrategyRunner.squashTimestamps(
            data, strategy.timeFrame
        )  # take into account the timeframe

        free_funds = strategy.capitalAllocation
        shares = 0.0

        for row in data:
            StrategyRunner.run_once(row, strategy, transactions, free_funds, shares)
            # add SL and TP here
        return transactions

    @staticmethod
    def squashTimestamps(data: List[tuple], timeframe: Timeframe):
        new_data = []
        index = 0
        bucket_time_start = datetime.combine(data[0][0], data[0][1])
        bucket_time_end = bucket_time_start + timedelta(
            minutes=TimeframeToMinutes[timeframe]
        )
        while index < len(data):
            date = data[index][0]
            time = data[index][1]
            open = data[index][2]
            high = data[index][3]
            low = data[index][4]
            close = data[index][5]
            spread = data[index][6]
            index += 1
            complete_candle = False
            while index < len(data):
                if datetime.combine(data[index][0], data[index][1]) >= bucket_time_end:
                    complete_candle = True
                    break
                high = max(high, data[index][3])
                low = min(low, data[index][4])
                close = data[index][5]
                spread = max(spread, data[index][6])
                index += 1
            if (
                not complete_candle
            ):  # excluding last candle if it is not complete. might want to include it in the future
                break
            new_data.append((date, time, open, high, low, close, spread))
            bucket_time_start = bucket_time_end
            bucket_time_end = bucket_time_start + timedelta(
                minutes=TimeframeToMinutes[timeframe]
            )

        return new_data

    @staticmethod
    def run_once(
        row: tuple,
        strategy: StrategyDetails,
        transactions: List[Transaction],
        free_funds: float,
        shares: float,
    ):
        if strategy.sellSignalMode == "DNF":
            StrategyRunner.run_once_DNF(
                row,
                strategy,
                transactions,
                free_funds,
                shares,
                TypeOfSignal.SELL,
            )
        else:
            StrategyRunner.run_once_CNF(
                row,
                strategy,
                transactions,
                free_funds,
                shares,
                TypeOfSignal.SELL,
            )

        if strategy.buySignalMode == "DNF":
            StrategyRunner.run_once_DNF(
                row,
                strategy,
                transactions,
                free_funds,
                shares,
                TypeOfSignal.BUY,
            )
        else:
            StrategyRunner.run_once_CNF(
                row,
                strategy,
                transactions,
                free_funds,
                shares,
                TypeOfSignal.BUY,
            )

    @staticmethod
    def canPlaceOrder(
        signalType: TypeOfSignal,
        strategy: StrategyDetails,
        free_funds: float,
        shares: float,
    ):
        if signalType == TypeOfSignal.BUY:
            if free_funds <= 0:
                return False
            if (
                strategy.exchangeBuyFee is not None
                and strategy.exchangeBuyFee.fixed is not None
                and strategy.exchangeBuyFee.fixed > free_funds
            ):
                return False
        else:
            if shares == 0:
                return False
        return True

    @staticmethod
    def run_once_CNF(
        row: tuple,
        strategy: StrategyDetails,
        transactions: List[Transaction],
        free_funds: float,
        shares: float,
        signalType: TypeOfSignal,
    ):
        date_time = datetime.combine(row[0], row[1])
        condition = True
        if signalType == TypeOfSignal.BUY:
            signals = strategy.buySignals
        else:
            signals = strategy.sellSignals

        for term in signals:
            termCondition = False
            for signal in term:
                if signal.operator == ">=":
                    termCondition = (
                        termCondition
                        or signal.indicator.calculateValue(date_time)
                        >= signal.threshold
                    )
                elif signal.operator == "<=":
                    termCondition = (
                        termCondition
                        or signal.indicator.calculateValue(date_time)
                        <= signal.threshold
                    )
                if termCondition == True:
                    break
            condition = condition and termCondition
            if condition == False:
                break

        if condition == True:
            StrategyRunner.place_order(
                signalType, strategy, transactions, free_funds, shares, row
            )

    @staticmethod
    def run_once_DNF(
        row: tuple,
        strategy: StrategyDetails,
        transactions: List[Transaction],
        free_funds: float,
        shares: float,
        signalType: TypeOfSignal,
    ):
        date_time = datetime.combine(row[0], row[1])
        condition = False
        if signalType == TypeOfSignal.BUY:
            signals = strategy.buySignals
        else:
            signals = strategy.sellSignals

        for term in signals:
            termCondition = True
            for signal in term:
                if signal.operator == ">=":
                    termCondition = (
                        termCondition
                        and signal.indicator.calculateValue(date_time)
                        >= signal.threshold
                    )
                elif signal.operator == "<=":
                    termCondition = (
                        termCondition
                        and signal.indicator.calculateValue(date_time)
                        <= signal.threshold
                    )
                if termCondition == False:
                    break
            condition = condition or termCondition
            if condition == True:
                break

        if condition == True:
            StrategyRunner.place_order(
                signalType, strategy, transactions, free_funds, shares, row
            )

    @staticmethod
    def place_order(
        signalType: TypeOfSignal,
        strategy: StrategyDetails,
        transactions: List[Transaction],
        free_funds: float,
        shares: float,
        row: tuple,
    ):
        if StrategyRunner.canPlaceOrder(signalType, strategy, free_funds, shares):
            if signalType == TypeOfSignal.BUY:
                used_money, fee = StrategyRunner.getUsedMoneyAndFee_BUY(
                    strategy, free_funds
                )
            else:
                used_money, fee = StrategyRunner.getUsedMoneyAndFee_SELL(
                    strategy, shares, row[5]
                )
            transactions.append(
                Transaction(
                    row[0], row[1], row[5], used_money / row[5], signalType, fee
                )
            )

    @staticmethod
    def getUsedMoneyAndFee_BUY(strategy: StrategyDetails, free_funds: float):
        if strategy.buySize.fixed is not None:
            used_money = min(free_funds, strategy.buySize.fixed)
        else:
            used_money = (
                free_funds * strategy.buySize.percentage
            )  # WARNING: might want to get percentage of free_funds + invested money

        if strategy.exchangeBuyFee is not None:
            if strategy.exchangeBuyFee.fixed is not None:
                used_money -= strategy.exchangeBuyFee.fixed
                fee = strategy.exchangeBuyFee.fixed
            else:
                used_money = used_money / (1 + strategy.exchangeBuyFee.percentage)
                fee = used_money * strategy.exchangeBuyFee.percentage
        else:
            fee = 0.0

        return used_money, fee

    @staticmethod
    def getUsedMoneyAndFee_SELL(strategy: StrategyDetails, shares: float, price: float):
        curr_invested_value = shares * price

        if strategy.sellSize.fixed is not None:
            used_money = min(curr_invested_value, strategy.sellSize.fixed)
        else:
            used_money = curr_invested_value * strategy.sellSize.percentage

        if strategy.exchangeSellFee is not None:
            if strategy.exchangeSellFee.fixed is not None:
                fee = strategy.exchangeSellFee.fixed
            else:
                fee = used_money * strategy.exchangeSellFee.percentage
        else:
            fee = 0.0

        return used_money, fee


# TODO (in far future):  add market order/ limit order/ stop order/ stop limit order
# TODO : set traded amount in money or in shares
