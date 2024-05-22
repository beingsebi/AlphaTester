from abc import ABC, abstractmethod
from datetime import datetime  # Abstract Base Class
from utils.constants import IndicatorNames, Timeframe


class BaseIndicator(ABC):
    # TODO: use a static buffer for data  ?? map<instrument,data>
    def __init__(
        self,
        instrumentName: str,
        indicatorName: IndicatorNames,
        timeframe: Timeframe = Timeframe.M1,
    ) -> None:
        if not instrumentName:
            raise ValueError("Instrument name is required")

        if not indicatorName:
            raise ValueError("Indicator name is required")

        self.instrumentName = instrumentName
        self.name = indicatorName
        self.timeframe = timeframe

    @abstractmethod
    def calculateValue(self, dateTime: datetime):
        pass

    @abstractmethod
    def __str__(self) -> str:
        return f"BaseIndicater: {self.name.name} | Timeframe: {self.timeframe.name}"
