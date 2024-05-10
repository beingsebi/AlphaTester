import json
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView

from utils.strategy.strategy import StrategyDetails

from .forms import StrategyForm
from .models import *


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
        except Exception as e:
            print("Error: " + str(e))
        return context


class StrategyResultView(generic.DetailView):
    model = Strategy
    template_name = "backtester/result.html"


class StrategyCreateView(CreateView):
    form_class = StrategyForm
    template_name = "backtester/strategy_form.html"

    def form_valid(self, form):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            return super().form_invalid(form)
        form.instance.user = self.request.user

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
                # TODO: Add signals where we finalize the implementation
                [],
                form.cleaned_data["sell_signal_mode"],
                [],
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

        context["x"] = json.dumps([1, 2, 3, 4, 5])
        context["y"] = json.dumps([1, 2, 4, 8, 16])
        return context
