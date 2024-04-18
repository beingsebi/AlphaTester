from django.urls import path

from .views import IndexListView, DetailView, ResultView, StrategyCreateView, StrategyDeleteView

app_name = "backtester"  # pylint: disable=C0103
#  because it is needed by Django

urlpatterns = [
    path("", IndexListView.as_view(), name="index-list"),
    path("detail/<int:pk>/", DetailView.as_view(), name="detail"),
    path("result/<int:pk>/", ResultView.as_view(), name="result"),
    path("strategy/add/", StrategyCreateView.as_view(), name="strategy-add"),
    path("strategy/<int:pk>/delete/",
         StrategyDeleteView.as_view(), name="strategy-delete"),
]
