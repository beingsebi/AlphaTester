from django import forms
from django.forms import ModelForm, formset_factory
from .models import Strategy
from utils.constants import (
    TIMEFRAME_CHOICES,
    SIGNALS_CHOICES,
    INDICATORS_CHOICES,
    TYPE_OF_SIGNAL_CHOICES,
    TYPE_OF_OPERATOR_CHOICES,
)


class PercentageFloatField(forms.FloatField):
    def clean(self, value):
        value = super().clean(value)
        if isinstance(value, str) and value.endswith("%"):
            # User entered a percentage with a % sign
            try:
                percentage = float(value[:-1])
                if not 0 <= percentage <= 100:
                    raise ValueError("Percentage must be between 0 and 100")
                return percentage / 100
            except ValueError:
                raise forms.ValidationError(
                    "Invalid percentage format. Enter a number between 0 and 100 or a value without a percentage sign."
                )
        return value


class IndicatorForm(forms.Form):
    indicator_name = forms.ChoiceField(choices=INDICATORS_CHOICES)
    value = forms.FloatField()
    operator = forms.ChoiceField(choices=TYPE_OF_OPERATOR_CHOICES)
    buy_or_sell = forms.ChoiceField(choices=TYPE_OF_SIGNAL_CHOICES)


IndicatorFormSet = formset_factory(form=IndicatorForm, extra=1)


class StrategyForm(ModelForm):
    # TODO: To decide which fields are required and which are not
    capital_allocation = forms.FloatField()
    bid_size = PercentageFloatField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter a value or percentage (e.g., 50%)"}
        )
    )
    time_frame = forms.ChoiceField(choices=TIMEFRAME_CHOICES)
    take_profit = PercentageFloatField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter a value or percentage (e.g., 50%)"}
        )
    )
    stop_loss = PercentageFloatField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter a value or percentage (e.g., 50%)"}
        )
    )
    exchange_fee = PercentageFloatField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter a value or percentage (e.g., 50%)"}
        )
    )
    # This field is always added for some reason
    indicators = formset_factory(form=IndicatorForm, extra=1)

    buy_signal_mode = forms.ChoiceField(choices=SIGNALS_CHOICES)
    sell_signal_mode = forms.ChoiceField(choices=SIGNALS_CHOICES)

    class Meta:
        model = Strategy
        # TODO: Remove unnecessary fields.
        fields = "__all__"
        # fields = [
        #     "capital_allocation",
        #     "bid_size",
        #     "time_frame",
        #     "take_profit",
        #     "stop_loss",
        #     "exchange_fee",
        #     "buy_signal_mode",
        #     "sell_signal_mode",
        # ]
