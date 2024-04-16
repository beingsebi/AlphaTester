class amount:
    def __init__(self, fixed: float | None, percentage: float | None = None) -> None:
        if fixed is not None and percentage is not None:
            raise ValueError("You can't have both fixed and percentage not None")
        if fixed is None and percentage is None:
            raise ValueError("You can't have both fixed and percentage None")
        self.fixed = fixed
        self.percentage = percentage
