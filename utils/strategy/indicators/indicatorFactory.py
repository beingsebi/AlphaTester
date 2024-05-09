from ... import constants
from .sma import SMA


class IndicatorFactory:  # pylint: disable=too-few-public-methods
    @staticmethod
    def createIndicator(indicatorName: constants.IndicatorNames, timeframe: constants.Timeframe, **kwargs):
        if indicatorName == constants.IndicatorNames.SMA:
            return SMA(indicatorName, timeframe, **kwargs)