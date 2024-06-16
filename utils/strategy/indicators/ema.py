from datetime import datetime, timedelta

from utils.constants import (IndicatorNames, Sources, SourcesToIndex, Timeframe,
                             TimeframeToMinutes)
from utils.database.get_instrument_data_scripts import get_data
from utils.strategyRunner.strategyRunner import StrategyRunner

from . import baseIndicator


class EMA(baseIndicator.BaseIndicator
         ):  # exponential moving average of previous `length` close prices

    def __init__(
            self,
            instrumentName: str,
            indicatorName: IndicatorNames,
            timeframe: Timeframe,
            **kwargs,  # length = 14, source = close
    ):
        """
        Initialize the EMA (Exponential Moving Average) indicator.

        Parameters:
        - name (str): The name of the indicator.
        - **kwargs: Additional keyword arguments.
            - length (int): The number of periods to consider (default: 14).
            - source (str): The source of the data (default: "close").

        Returns:
        None
        """
        super().__init__(instrumentName, indicatorName, timeframe)
        _kwargs = kwargs.copy()  # just in case we need it later in the caller
        self.length = _kwargs.pop("length", 14)
        self.source = _kwargs.pop("source",
                                  Sources.CLOSE)  # default source is close
        if _kwargs:
            raise ValueError(f"Invalid keyword arguments: {_kwargs}")

    # override the abstract calculateValue method
    def calculateValue(self, dateTime: datetime):
        startDateTime = dateTime - timedelta(minutes=self.length *
                                             TimeframeToMinutes[self.timeframe])
        data = get_data(
            self.instrumentName,
            startDateTime,
            dateTime,
        )
        if not data:
            return None
        data = StrategyRunner.squashTimestamps(data, self.timeframe)

        index = SourcesToIndex[self.source]
        alpha = 2 / (self.length + 1)
        ema = data[0][index]  # initialize EMA with first value
        for i in range(1, len(data)):
            ema = alpha * data[i][index] + (1 - alpha) * ema
        return ema

    def __str__(self) -> str:
        return f"{super().__str__()}" f" (length: {self.length} | source: {self.source})"

    def __repr__(self) -> str:
        return f"{super().__str__()}" f" (length: {self.length} | source: {self.source})"
