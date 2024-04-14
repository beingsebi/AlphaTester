from django.http import HttpResponse
from django.views import generic
from .models import Strategy

class IndexView(generic.ListView):
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