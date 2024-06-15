from django.db import models
from django.urls import reverse


class Strategy(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    instrument = models.ForeignKey("Instrument",
                                   on_delete=models.SET_NULL,
                                   null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    strategyDetails = models.JSONField(null=True)
    results = models.JSONField(null=True)

    def __str__(self):
        return self.name + " by " + self.user.username

    def get_absolute_url(self):  # pylint: disable=C0103
        #   because it is a Django method
        return reverse("backtester:detail", kwargs={"pk": self.pk})


class Instrument(models.Model):
    """
    Represents a financial instrument.

    Attributes:
        name (str): The name of the instrument.
        symbol (str): The symbol of the instrument.
        exchange (str): The exchange where the instrument is traded.
        currency (str): The currency in which the instrument is traded.
        type (str): The type of the instrument.
        description (str): A description of the instrument.
    """

    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    exchange = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField(default="No description provided.")

    def __str__(self):
        return self.name + " (" + self.symbol + ")"
