from abc import ABC, abstractmethod  # Abstract Base Class

import sqlalchemy

from ... import constants


class BaseIndicator(ABC):
    def __init__(self, name: str, timeframe: constants.Timeframe) -> None:
        if not name:
            raise ValueError("Indicator name is required")

        if name.lower() not in constants.supportedIndicators:
            raise ValueError("Invalid indicator name")

        self.name = name
        self.timeframe = timeframe

    @abstractmethod
    def calculateValue(self, date: sqlalchemy.types.Date, time: sqlalchemy.types.Time):
        pass
