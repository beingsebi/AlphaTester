from abc import ABC, abstractmethod  # Abstract Base Class

import sqlalchemy

from ... import constants


class BaseIndicator(ABC):
    # TODO: use a static buffer for data  ?? map<instrument,data>
    def __init__(self, instrumentName: str, indicatorName: constants.IndicatorNames, timeframe: constants.Timeframe = constants.Timeframe.M1) -> None:
        if not instrumentName:
            raise ValueError("Instrument name is required")

        if not indicatorName:
            raise ValueError("Indicator name is required")

        self.instrumentName = instrumentName
        self.name = indicatorName
        self.timeframe = timeframe

    @abstractmethod
    def calculateValue(self, date: sqlalchemy.types.Date, time: sqlalchemy.types.Time):
        pass

    @abstractmethod
    def __str__(self) -> str:
        return f"BaseIndicater: {self.name.name} | Timeframe: {self.timeframe.name}"
