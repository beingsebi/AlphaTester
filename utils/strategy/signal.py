from ..constants import IndicatorNames


class Signal:
    def __init__(self, indicatorName: IndicatorNames, value: float, operator: str, **indicatorArgs) -> None:
        # here will also check if indicator is valid
        self.indicator = indicatorName
        self.value = value
        # value might become Amount type if necessary
        self.operator = operator  # "<=" or ">="
        self.indicatorArgs = indicatorArgs
