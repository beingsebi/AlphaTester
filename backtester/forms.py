import datetime

from django import forms
from django.forms import ModelForm, formset_factory

from utils.constants import (INDICATORS_CHOICES, SIGNALS_CHOICES,
                             SOURCES_CHOICES, TIMEFRAME_CHOICES,
                             TYPE_OF_OPERATOR_CHOICES, TYPE_OF_SIGNAL_CHOICES,
                             Sources)
from utils.strategy.amount import Amount

from .models import Strategy


class PercentageFloatField(forms.FloatField):

    def clean(self, value):
        # value = super().clean(value)
        if isinstance(value, str) and value.endswith("%"):
            # User entered a percentage with a % sign
            try:
                percentage = float(value[:-1])
                if not 0 <= percentage <= 100:
                    raise ValueError("Percentage must be between 0 and 100")
                return Amount(None, percentage / 100)
            except ValueError:
                raise forms.ValidationError(
                    "Invalid percentage format. Enter a number between 0 and 100 or a value without a percentage sign."
                )
        return Amount(float(value))


# class IndicatorForm(forms.Form):
#     indicator_name = forms.ChoiceField(choices=INDICATORS_CHOICES)
#     value = forms.FloatField()
#     operator = forms.ChoiceField(choices=TYPE_OF_OPERATOR_CHOICES)
#     buy_or_sell = forms.ChoiceField(choices=TYPE_OF_SIGNAL_CHOICES)


class IndicatorForm(forms.Form):
    indicator_name = forms.ChoiceField(choices=INDICATORS_CHOICES)
    timeframe = forms.ChoiceField(choices=TIMEFRAME_CHOICES)
    length = forms.IntegerField()
    source = forms.ChoiceField(choices=SOURCES_CHOICES)
    threshold = forms.FloatField()
    operator = forms.ChoiceField(choices=TYPE_OF_OPERATOR_CHOICES)
    buy_or_sell = forms.ChoiceField(choices=TYPE_OF_SIGNAL_CHOICES)


IndicatorFormSet = formset_factory(form=IndicatorForm, extra=1)
# todo here too i think


class StrategyForm(ModelForm):
    # TODO: To decide which fields are required and which are not
    capital_allocation = forms.FloatField()

    timeframe = forms.ChoiceField(choices=TIMEFRAME_CHOICES)

    buy_size = PercentageFloatField(widget=forms.TextInput(
        attrs={"placeholder": "Enter a value or percentage (e.g., 50%)"}))

    sell_size = PercentageFloatField(widget=forms.TextInput(
        attrs={"placeholder": "Enter a value or percentage (e.g., 50%)"}))

    take_profit = PercentageFloatField(widget=forms.TextInput(
        attrs={"placeholder": "Enter a value or percentage (e.g., 50%)"}))

    stop_loss = PercentageFloatField(widget=forms.TextInput(
        attrs={"placeholder": "Enter a value or percentage (e.g., 50%)"}))

    buy_signal_mode = forms.ChoiceField(choices=SIGNALS_CHOICES)

    sell_signal_mode = forms.ChoiceField(choices=SIGNALS_CHOICES)

    # todo important: signals

    exchange_buy_fee = PercentageFloatField(widget=forms.TextInput(
        attrs={"placeholder": "Enter a value or percentage (e.g., 50%)"}))

    exchange_sell_fee = PercentageFloatField(widget=forms.TextInput(
        attrs={"placeholder": "Enter a value or percentage (e.g., 50%)"}))

    start_datetime = forms.DateTimeField(widget=forms.DateTimeInput(),
                                         initial=datetime.datetime.now())
    end_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput,
        initial=datetime.datetime.now() - datetime.timedelta(days=365),
    )
    # This field is always added for some reason
    indicators = formset_factory(form=IndicatorForm, extra=1)

    class Meta:
        model = Strategy
        # TODO: Remove unnecessary fields.
        # fields = "__all__"
        fields = [
            "name",
            "description",
            "instrument",
            "capital_allocation",
            "timeframe",
            "buy_size",
            "sell_size",
            "take_profit",
            "stop_loss",
            "buy_signal_mode",
            "sell_signal_mode",
            "exchange_buy_fee",
            "exchange_sell_fee",
            "start_datetime",
            "end_datetime",
        ]
