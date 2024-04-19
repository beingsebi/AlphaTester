import sqlalchemy
from . import baseIndicator
from ... import constants


class SMA(baseIndicator.BaseIndicator):
    def __init__(self, indicatorName: constants.Indicators, timeframe: constants.Timeframe, **kwargs):
        """
        Initialize the SMA (Simple Moving Average) indicator.

        Parameters:
        - name (str): The name of the indicator.
        - **kwargs: Additional keyword arguments.
            - length (int): The number of periods to consider (default: 14).
            - source (str): The source of the data (default: "close").

        Returns:
        None
        """
        super().__init__(indicatorName, timeframe)
        _kwargs = kwargs.copy()  # just in case we need it later in the caller
        self.length = _kwargs.pop("length", 14)
        self.close = _kwargs.pop("source", constants.Sources.CLOSE)
        if _kwargs:
            raise ValueError(f"Invalid keyword arguments: {_kwargs}")

    # override the abstract calculateValue method
    def calculateValue(self, date: sqlalchemy.types.Date, time: sqlalchemy.types.Time):
        # might change the types
        pass
