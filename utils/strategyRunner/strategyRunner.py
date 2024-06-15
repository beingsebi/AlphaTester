from typing import List

from datetime import date, datetime, time, timedelta
from utils.constants import Timeframe, TimeframeToMinutes, TypeOfSignal
from utils.database.get_instrument_data_scripts import (
    get_data,
    get_last_available_date,
    get_first_available_date,
)
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
        return f"{self.date} {self.time} {self.price} {self.quantity} {self.type.name} {self.fee}"

    def __repr__(self) -> str:
        return f"{self.date} {self.time} {self.price} {self.quantity} {self.type.name} {self.fee}"


class TradingState:

    def __init__(self, free_funds: float, shares: float, medium_price: float):
        self.free_funds = free_funds
        self.shares = shares
        self.medium_price = medium_price


class StrategyRunner:

    @staticmethod
    def run(strategy: StrategyDetails) -> List[Transaction]:
        transactions = []
        # TODO IMPORTANT: now assuming trading starts late enough to have enough data for all indicators
        # TODO: add squash transactions flag (if buy and sell at same time, then squash them into one transaction)
        # WARNING: for now, the transaction will buy/sell the close price

        #! IMPORTANT: here will modify strategy details
        StrategyRunner.fixStartDatetime(strategy)
        StrategyRunner.fixEndDatetime(strategy)

        print("-----")
        print(strategy.startDatetime)
        print(strategy.endDatetime)
        print("-----")

        if strategy.startDatetime >= strategy.endDatetime:
            raise Exception(
                "Actual start date of candle is greater than or equal to the actual end date of candle."
            )

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
            data, strategy.timeFrame)  # take into account the timeframe

        tradingState = TradingState(strategy.capitalAllocation, 0.0, 0.0)

        for row in data:
            old_len = len(transactions)
            old_shares = tradingState.shares
            if tradingState.shares > 0:  # TP and SL
                if row[5] > tradingState.medium_price:
                    if strategy.takeProfit is not None:
                        if strategy.takeProfit.fixed is not None:
                            if (row[5] >= tradingState.medium_price +
                                    strategy.takeProfit.fixed):
                                StrategyRunner.liquidate_all(
                                    row, transactions, strategy,
                                    tradingState.shares)
                                tradingState.shares = 0
                        elif strategy.takeProfit.percentage is not None:
                            if row[5] >= tradingState.medium_price * (
                                    1 + strategy.takeProfit.percentage):
                                StrategyRunner.liquidate_all(
                                    row, transactions, strategy,
                                    tradingState.shares)
                                tradingState.shares = 0
                elif row[5] < tradingState.medium_price:
                    if strategy.stopLoss is not None:
                        if strategy.stopLoss.fixed is not None:
                            if (row[5] <= tradingState.medium_price -
                                    strategy.stopLoss.fixed):
                                StrategyRunner.liquidate_all(
                                    row, transactions, strategy,
                                    tradingState.shares)
                                tradingState.shares = 0
                        elif strategy.stopLoss.percentage is not None:
                            if row[5] <= tradingState.medium_price * (
                                    1 - strategy.stopLoss.percentage):
                                StrategyRunner.liquidate_all(
                                    row, transactions, strategy,
                                    tradingState.shares)
                                tradingState.shares = 0

            StrategyRunner.run_once(row, strategy, transactions, tradingState)
            if (  # for TP and SL
                    len(transactions) > old_len
                    and transactions[-1].type == TypeOfSignal.BUY):
                if old_shares + transactions[-1].quantity == 0:
                    tradingState.medium_price = 0
                else:
                    tradingState.medium_price = (
                        old_shares * tradingState.medium_price +
                        transactions[-1].price * transactions[-1].quantity) / (
                            old_shares + transactions[-1].quantity)

        if tradingState.shares > 0:
            StrategyRunner.liquidate_all(  # liquidate all at the end | WARNING: might want to change this
                data[-1], transactions, strategy, tradingState.shares)
        return transactions

    @staticmethod
    def squashTimestamps(data: List[tuple], timeframe: Timeframe):
        new_data = []
        index = 0
        bucket_time_start = datetime.combine(data[0][0], data[0][1])
        bucket_time_end = bucket_time_start + timedelta(
            minutes=TimeframeToMinutes[timeframe])
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
                if datetime.combine(data[index][0],
                                    data[index][1]) >= bucket_time_end:
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
                minutes=TimeframeToMinutes[timeframe])

        return new_data

    @staticmethod
    def run_once(
        row: tuple,
        strategy: StrategyDetails,
        transactions: List[Transaction],
        tradingState: TradingState,
    ):
        if strategy.sellSignalMode == "DNF":
            StrategyRunner.run_once_DNF(
                row,
                strategy,
                transactions,
                tradingState,
                TypeOfSignal.SELL,
            )
        else:
            StrategyRunner.run_once_CNF(
                row,
                strategy,
                transactions,
                tradingState,
                TypeOfSignal.SELL,
            )

        if strategy.buySignalMode == "DNF":
            StrategyRunner.run_once_DNF(
                row,
                strategy,
                transactions,
                tradingState,
                TypeOfSignal.BUY,
            )
        else:
            StrategyRunner.run_once_CNF(
                row,
                strategy,
                transactions,
                tradingState,
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
            if (strategy.exchangeBuyFee is not None
                    and strategy.exchangeBuyFee.fixed is not None
                    and strategy.exchangeBuyFee.fixed > free_funds):
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
        tradingState: TradingState,
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
                    termCondition = termCondition or (
                        signal.indicator.calculateValue(date_time)
                        >= signal.threshold)
                elif signal.operator == "<=":
                    termCondition = termCondition or (
                        signal.indicator.calculateValue(date_time)
                        <= signal.threshold)
                if termCondition == True:
                    break
            condition = condition and termCondition
            if condition == False:
                break

        if condition == True:
            StrategyRunner.place_order(signalType, strategy, transactions,
                                       tradingState, row)

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
                    termCondition = termCondition and (
                        signal.indicator.calculateValue(date_time)
                        >= signal.threshold)
                elif signal.operator == "<=":
                    termCondition = termCondition and (
                        signal.indicator.calculateValue(date_time)
                        <= signal.threshold)
                if termCondition == False:
                    break
            condition = condition or termCondition
            if condition == True:
                break

        if condition == True:
            StrategyRunner.place_order(signalType, strategy, transactions,
                                       free_funds, shares, row)

    @staticmethod
    def place_order(
        signalType: TypeOfSignal,
        strategy: StrategyDetails,
        transactions: List[Transaction],
        tradingState: TradingState,
        row: tuple,
    ):
        if StrategyRunner.canPlaceOrder(signalType, strategy,
                                        tradingState.free_funds,
                                        tradingState.shares):
            if signalType == TypeOfSignal.BUY:
                used_money, fee = StrategyRunner.getUsedMoneyAndFee_BUY(
                    strategy, tradingState.free_funds)
            else:
                used_money, fee = StrategyRunner.getUsedMoneyAndFee_SELL(
                    strategy, tradingState.shares, row[5])
            if signalType == TypeOfSignal.BUY:
                tradingState.shares += used_money / row[5]
                tradingState.free_funds -= used_money + fee
            else:
                tradingState.shares -= used_money / row[5]
                tradingState.free_funds += used_money - fee
            transactions.append(
                Transaction(row[0], row[1], row[5], used_money / row[5],
                            signalType, fee))

    @staticmethod
    def getUsedMoneyAndFee_BUY(strategy: StrategyDetails, free_funds: float):
        if strategy.buySize.fixed is not None:
            used_money = min(free_funds, strategy.buySize.fixed)
        else:
            used_money = free_funds * strategy.buySize.percentage

        if strategy.exchangeBuyFee is not None:
            if strategy.exchangeBuyFee.fixed is not None:
                used_money -= strategy.exchangeBuyFee.fixed
                fee = strategy.exchangeBuyFee.fixed
            else:
                used_money = used_money / (1 +
                                           strategy.exchangeBuyFee.percentage)
                fee = used_money * strategy.exchangeBuyFee.percentage
        else:
            fee = 0.0

        return used_money, fee

    @staticmethod
    def getUsedMoneyAndFee_SELL(strategy: StrategyDetails, shares: float,
                                price: float):
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

    @staticmethod
    def liquidate_all(
        row: tuple,
        transactions: List[Transaction],
        strategy: StrategyDetails,
        shares: float,
    ):
        if strategy.exchangeSellFee is None:
            fee = 0
        elif strategy.exchangeSellFee.fixed is not None:
            fee = strategy.exchangeSellFee.fixed
        else:
            fee = shares * row[5] * strategy.exchangeSellFee.percentage

        transactions.append(
            Transaction(row[0], row[1], row[5], shares, TypeOfSignal.SELL,
                        fee))

    @staticmethod
    def fixStartDatetime(strategy: StrategyDetails):
        firstAvailableDate = get_first_available_date(strategy.instrumentName)
        print("ee " + str(firstAvailableDate))
        if firstAvailableDate is None:
            raise Exception("No data found")
        maxim = 0
        for i in strategy.indicators:
            if hasattr(i, "length") and i.timeframe is not None:
                maxim = max(maxim,
                            (i.length + 1) * TimeframeToMinutes[i.timeframe])
        firstAvailableDate += timedelta(minutes=maxim)
        strategy.startDatetime = max(strategy.startDatetime,
                                     firstAvailableDate)
        while True:
            if StrategyRunner.isCandleDateValid(strategy.startDatetime,
                                                strategy.timeFrame):
                break
            strategy.startDatetime += timedelta(minutes=1)

    @staticmethod
    def fixEndDatetime(strategy: StrategyDetails):

        lastAvailableDate = get_last_available_date(strategy.instrumentName)
        if lastAvailableDate is None:
            raise Exception("No data found")
        strategy.endDatetime = min(strategy.endDatetime, lastAvailableDate)
        while True:
            if StrategyRunner.isCandleDateValid(strategy.endDatetime,
                                                strategy.timeFrame):
                break
            strategy.endDatetime -= timedelta(minutes=1)

    @staticmethod
    def isCandleDateValid(dateTime: datetime, timeFrame: Timeframe):
        if dateTime == None or timeFrame == Timeframe.M1:
            return True

        start_hour = dateTime.hour
        start_minute = dateTime.minute

        if timeFrame == Timeframe.M5:
            return start_minute % 5 == 0

        if timeFrame == Timeframe.M15:
            return start_minute % 15 == 0

        if timeFrame == Timeframe.M30:
            return start_minute % 30 == 0

        if timeFrame == Timeframe.H1:
            return start_minute == 0

        if timeFrame == Timeframe.H4:
            return (start_minute == 0 and start_hour % 4 == 2
                    )  # might want to change here the modulo

        if timeFrame == Timeframe.D1:
            return start_minute == 0 and start_hour == 0

        if timeFrame == Timeframe.W1:
            return start_minute == 0 and start_hour == 0 and dateTime.weekday(
            ) == 0

        if timeFrame == Timeframe.MN1:
            return start_minute == 0 and start_hour == 0 and dateTime.day == 1
        return False


# TODO (in far future):  add market order/ limit order/ stop order/ stop limit order
# TODO : set traded amount in money or in shares
