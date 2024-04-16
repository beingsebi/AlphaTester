class Signal:
    def __init__(self, indicator: str, value: float, operator: str) -> None:
        # here will also check if indicator is valid
        self.indicator = indicator
        self.value = value
        # value might become Amount type if necessary
        self.operator = operator  # "<=" or ">="
