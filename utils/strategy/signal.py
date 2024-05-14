from ..constants import IndicatorNames, TypeOfOpOperatorChoices


class Signal:
    def __init__(
        self,
        indicatorName: IndicatorNames,
        value: float,
        operator: TypeOfOpOperatorChoices,
        **indicatorArgs,
    ) -> None:
        # TODO: here will also check if indicator is valid
        self.indicator = indicatorName
        self.value = value
        # value might become Amount type if necessary
        self.operator = operator  # "<=" or ">="
        self.indicatorArgs = indicatorArgs

    def __str__(self) -> str:
        return f"{self.indicator} {self.operator} {self.value}"

    def __repr__(self) -> str:
        return f"{self.indicator} {self.operator} {self.value}"
