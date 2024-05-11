import json
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

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
        buySignals = []
        sellSignals = []
        context = self.get_context_data()
        indicators = context["indicators"]
        if indicators.is_valid():
            indicators.instance = self.object
            for indicator_form in indicators:
                if indicator_form.is_valid():
                    signal = Signal(
                        indicator_form.cleaned_data["indicator_name"],
                        indicator_form.cleaned_data["value"],
                        indicator_form.cleaned_data["operator"],
                    )
                    if indicator_form.cleaned_data["buy_or_sell"] == "BUY":
                        buySignals.append(signal)
                    else:
                        sellSignals.append(signal)
        else:
            return self.render_to_response(self.get_context_data(form=form))

        # We try to create a StrategyDetails object from the form data
        # If we fail, we add an error to the form and return the invalid form
        # Otherwise, we convert the StrategyDetails object to JSON and save it in the form instance
        try:
            strategyDetails = StrategyDetails(
                form.cleaned_data["capital_allocation"],
                form.cleaned_data["bid_size"],
                form.cleaned_data["time_frame"],
                form.cleaned_data["take_profit"],
                form.cleaned_data["stop_loss"],
                form.cleaned_data["exchange_fee"],
                form.cleaned_data["buy_signal_mode"],
                buySignals,
                form.cleaned_data["sell_signal_mode"],
                sellSignals,
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
        # x: date.valueOf(),
        # o: open,
        # h: high,
        # l: low,
        # c: close
        context["data"] = json.dumps(
            [
                {"x": 1715621935000, "o": 30.92, "h": 31.94, "l": 27.38, "c": 29.71},
                {"x": 1715708335000, "o": 29.55, "h": 32.44, "l": 28.07, "c": 28.17},
                {"x": 1715794735000, "o": 29.08, "h": 32.27, "l": 27.09, "c": 30.27},
                {"x": 1715881135000, "o": 29.83, "h": 32.29, "l": 26.93, "c": 28.93},
                {"x": 1715967535000, "o": 27.98, "h": 29.79, "l": 26.89, "c": 27.85},
                {"x": 1716226735000, "o": 28.69, "h": 30.48, "l": 25.14, "c": 27.51},
                {"x": 1716313135000, "o": 27.95, "h": 30.56, "l": 25.24, "c": 27.26},
                {"x": 1716399535000, "o": 28.62, "h": 31.15, "l": 26.32, "c": 28.79},
                {"x": 1716485935000, "o": 27.78, "h": 28.3, "l": 26.5, "c": 27.01},
                {"x": 1716572335000, "o": 27.45, "h": 29.15, "l": 25.31, "c": 26.47},
                {"x": 1716831535000, "o": 27.38, "h": 27.47, "l": 25.4, "c": 26.02},
            ]
        )
        context["x"] = json.dumps([1, 2, 3, 4, 5])
        context["y"] = json.dumps([1, 2, 4, 8, 16])
        return context


class UpdateStrategy(UpdateView):
    model = Strategy
    template_name = "backtester/update.html"
    fields = "__all__"
