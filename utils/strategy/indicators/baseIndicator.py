from abc import ABC, abstractmethod  # Abstract Base Class

import sqlalchemy

from ... import constants


class BaseIndicator(ABC):
    def __init__(self, indicatorName: constants.IndicatorNames, timeframe: constants.Timeframe) -> None:
        if not indicatorName:
            raise ValueError("Indicator name is required")

        self.name = indicatorName
        self.timeframe = timeframe

    @abstractmethod
    def calculateValue(self, date: sqlalchemy.types.Date, time: sqlalchemy.types.Time):
        pass
