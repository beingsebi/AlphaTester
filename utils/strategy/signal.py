from utils.strategy.indicators.baseIndicator import BaseIndicator
from utils.constants import TypeOfOpOperatorChoices


class Signal:
    def __init__(
            self,
            indicator: BaseIndicator,
            value: float,
            operator: TypeOfOpOperatorChoices) -> None:
        self.indicator = indicator
        self.value = value
        # value might become Amount type if necessary
        self.operator = operator  # "<=" or ">="

    def __str__(self) -> str:
        return f"{self.indicator}  |  {self.operator} {self.value}"

    def __repr__(self) -> str:
        return f"{self.indicator}  |  {self.operator} {self.value}"
