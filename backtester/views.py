from django.views import generic
from .models import Strategy
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy

class IndexListView(generic.ListView):
    template_name = "backtester/index.html"
    context_object_name = "latest_strategy_list"

    def get_queryset(self):
        """Return the last five published strategies."""
        return Strategy.objects.order_by("-created_at")[:5]

class DetailView(generic.DetailView):
    model = Strategy
    template_name = "backtester/detail.html"
    
class ResultView(generic.DetailView):
    model = Strategy
    template_name = "backtester/result.html"
    
class StrategyCreateView(CreateView):
    model = Strategy
    template_name = "backtester/strategy_form.html"
    fields = ["name", "description"] # Only these fields are shown in the form
    
    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return super().form_invalid(form)
        form.instance.user = self.request.user
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