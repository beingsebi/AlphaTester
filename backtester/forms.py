from django import forms
from django.forms import ModelForm
from .models import Strategy

TIMEFRAME_CHOICES = [
    ('1m', '1m'),
    ('5m', '5m'),
    ('15m', '15m'),
    ('30m', '30m'),
    ('1h', '1h'),
    ('4h', '4h'),
    ('1d', '1d'),
    ('1w', '1w'),
    ('1M', '1M'),
]

SIGNALS_CHOICES = [
    ('CNF', 'CNF'),
    ('DNF', 'DNF'),
]


class PercentageFloatField(forms.FloatField):
    def clean(self, value):
        value = super().clean(value)
        if isinstance(value, str):
            # User entered a percentage with a % sign
            try:
                percentage = float(value[:-1])
                if not 0 <= percentage <= 100:
                    raise ValueError("Percentage must be between 0 and 100")
                return percentage / 100
            except ValueError as ve:
                raise forms.ValidationError(
                    "Invalid percentage format. Enter a number between 0"
                    + " and 100 or a value without a percentage sign.") from ve
        return value


class StrategyForm(ModelForm):
    # TODO: To decide which fields are required and which are not
    capital_allocation = forms.FloatField()
    bid_size = PercentageFloatField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter a value or percentage (e.g., 50%)'}))
    time_frame = forms.ChoiceField(choices=TIMEFRAME_CHOICES)
    take_profit = PercentageFloatField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter a value or percentage (e.g., 50%)'}))
    stop_loss = PercentageFloatField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter a value or percentage (e.g., 50%)'}))
    exchange_fee = PercentageFloatField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter a value or percentage (e.g., 50%)'}))
    buy_signal_mode = forms.ChoiceField(choices=SIGNALS_CHOICES)
    sell_signal_mode = forms.ChoiceField(choices=SIGNALS_CHOICES)

    class Meta:
        model = Strategy
        # TODO: Remove unnecessary fields.
        fields = "__all__"
