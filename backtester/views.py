from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from utils.strategy.strategy import StrategyDetails
from utils.strategy.signal import Signal

from .forms import *
from .models import Strategy
from django.views.generic.edit import FormView


class IndexListView(generic.ListView):
    template_name = "backtester/index.html"
    context_object_name = "latest_strategy_list"

    def get_queryset(self):
        """Return the last five published strategies."""
        return Strategy.objects.order_by("-created_at")[:5]


class DetailView(generic.DetailView):
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


class ResultView(generic.DetailView):
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
                    buySignal = Signal(
                        indicator_form.cleaned_data["type"],
                        indicator_form.cleaned_data["buy_treshold"],
                        ">=",
                    )
                    buySignals.append(buySignal)

                    sellSignal = Signal(
                        indicator_form.cleaned_data["type"],
                        indicator_form.cleaned_data["sell_treshold"],
                        "<=",
                    )
                    sellSignals.append(sellSignal)
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


# https://aalvarez.me/posts/django-formsets-with-generic-formviews/
class UpdateStrategy(UpdateView):
    model = Strategy
    template_name = "backtester/update.html"
    fields = "__all__"
