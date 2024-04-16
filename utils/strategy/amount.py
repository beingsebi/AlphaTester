class amount:
    def __init__(self, fixed: float | None, percentage: float | None = None) -> None:
        if fixed is not None and percentage is not None:
            raise ValueError("You can't have both fixed and percentage not None")

        if fixed is None and percentage is None:
            raise ValueError("You can't have both fixed and percentage None")

        if self.percentage is not None and not (
            self.percentage >= 0 and self.percentage <= 100
        ):
            raise ValueError("Percentage must be between 0 and 100")

        self.fixed = fixed
        self.percentage = percentage
