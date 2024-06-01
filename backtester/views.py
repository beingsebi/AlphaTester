import json
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from utils.strategy.indicators.indicatorFactory import IndicatorFactory
from utils.strategy.strategy import StrategyDetails
from utils.strategy.signal import Signal

from .forms import *
from .models import *
from django.views.generic.edit import FormView


class StrategyListView(generic.ListView):
    template_name = "backtester/index.html"
    context_object_name = "latest_strategy_list"

    def get_queryset(self):
        """Return the last five published strategies."""
        return Strategy.objects.order_by("-created_at")[:5]


class StrategyDetailView(generic.DetailView):
    model = Strategy
    template_name = "backtester/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["strategyDetails"] = StrategyDetails.fromJSON(
                self.object.strategyDetails
            )
            print(context["strategyDetails"])
        except Exception as e:
            print("Error: " + str(e))
        return context


class StrategyResultView(generic.DetailView):
    model = Strategy
    template_name = "backtester/result.html"


class StrategyCreateView(CreateView):
    form_class = StrategyForm
    template_name = "backtester/strategy_form.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["indicators"] = IndicatorFormSet(self.request.POST)
        else:
            data["indicators"] = IndicatorFormSet()
        return data

    def form_valid(self, form):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            return super().form_invalid(form)
        form.instance.user = self.request.user

        # Parse the indicators. If the formset is invalid, we return the invalid formset.
        # buySignals = []
        # sellSignals = []
        indicator_instances = []
        context = self.get_context_data()
        indicators = context["indicators"]
        if indicators.is_valid():
            indicators.instance = self.object
            for indicator_form in indicators:
                if indicator_form.is_valid():
                    print(indicator_form.cleaned_data["indicator_name"])
                    indicator = IndicatorFactory.createIndicator(
                        indicator_form.cleaned_data["instrument_name"],
                        indicator_form.cleaned_data["indicator_name"],
                        indicator_form.cleaned_data["timeframe"],
                        length=indicator_form.cleaned_data["length"],
                        source=indicator_form.cleaned_data["source"],
                    )
                    indicator_instances.append(indicator)
                    # signal = Signal(
                    #     # TODO: refactor
                    #     indicator_form.cleaned_data["indicator_name"],
                    #     indicator_form.cleaned_data["value"],
                    #     indicator_form.cleaned_data["operator"],
                    # )
                    # if indicator_form.cleaned_data["buy_or_sell"] == "BUY":
                    #     buySignals.append(signal)
                    # else:
                    #     sellSignals.append(signal)
        else:
            return self.render_to_response(self.get_context_data(form=form))
        print(indicator_instances)
        # We try to create a StrategyDetails object from the form data
        # If we fail, we add an error to the form and return the invalid form
        # Otherwise, we convert the StrategyDetails object to JSON and save it in the form instance
        try:
            strategyDetails = StrategyDetails(
                form.cleaned_data["instrument"],
                form.cleaned_data["capital_allocation"],
                form.cleaned_data["timeframe"],
                form.cleaned_data["buy_size"],
                form.cleaned_data["sell_size"],
                form.cleaned_data["take_profit"],
                form.cleaned_data["stop_loss"],
                indicator_instances,  # TOOD indicators
                form.cleaned_data["buy_signal_mode"],
                [],  # buySignals,
                form.cleaned_data["sell_signal_mode"],
                [],  # sellSignals,
                form.cleaned_data["exchange_buy_fee"],
                form.cleaned_data["exchange_sell_fee"],
                form.cleaned_data["start_datetime"],
                form.cleaned_data["end_datetime"],
            )
            form.instance.strategyDetails = StrategyDetails.toJSON(strategyDetails)

        except Exception as e:
            # TODO: Add logging and replace prints.
            print("Instanta " + str(form.instance.strategyDetails))
            print("Eroare " + str(e))
            form.add_error("strategyDetails", str(e))
            return super().form_invalid(form)

        return super().form_valid(form)


class StrategyDeleteView(DeleteView):
    model = Strategy
    template_name = "backtester/strategy_confirm_delete.html"
    success_url = reverse_lazy("backtester:index-list")

    def form_valid(self, form):
        # Check if the user is the owner of the strategy
        if self.request.user != self.object.user:
            return super().form_invalid(form)

        return super().form_valid(form)


class InstrumentDetailView(generic.DetailView):
    model = Instrument
    template_name = "backtester/instrument_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["symbol"] = self.object.name
        return context


class UpdateStrategy(UpdateView):
    model = Strategy
    template_name = "backtester/update.html"
    fields = "__all__"
