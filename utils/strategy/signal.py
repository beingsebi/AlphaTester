from utils.constants import TypeOfOpOperatorChoices
from utils.strategy.indicators.baseIndicator import BaseIndicator


class Signal:

    def __init__(
        self,
        indicator: BaseIndicator,
        threshold: float,
        operator: TypeOfOpOperatorChoices,
    ) -> None:
        self.indicator = indicator
        self.threshold = threshold
        # threshold might become Amount type if necessary
        self.operator = operator  # "<=" or ">="

    def __str__(self) -> str:
        return f"{self.indicator}  |  {self.operator} {self.threshold}"

    def __repr__(self) -> str:
        return f"{self.indicator}  |  {self.operator} {self.threshold}"
