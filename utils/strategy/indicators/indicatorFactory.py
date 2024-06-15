from utils.constants import IndicatorNames, Timeframe

from .ema import EMA
from .sma import SMA


class IndicatorFactory:  # pylint: disable=too-few-public-methods

    @staticmethod
    def createIndicator(
        instrumentName: str,
        indicatorName: IndicatorNames,
        timeframe: Timeframe,
        **kwargs,
    ):
        if indicatorName == IndicatorNames.SMA:
            return SMA(instrumentName, indicatorName, timeframe, **kwargs)
        if indicatorName == IndicatorNames.EMA:
            return EMA(instrumentName, indicatorName, timeframe, **kwargs)
