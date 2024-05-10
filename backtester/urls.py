from django.urls import path

from .models import Instrument
from .views import *
from django.views import generic

app_name = "backtester"  # pylint: disable=C0103
#  because it is needed by Django

urlpatterns = [
    path("", StrategyListView.as_view(), name="index-list"),
    path("detail/<int:pk>/", StrategyDetailView.as_view(), name="detail"),
    path("result/<int:pk>/", StrategyResultView.as_view(), name="result"),
    path("strategy/add/", StrategyCreateView.as_view(), name="strategy-add"),
    path(
        "strategy/<int:pk>/delete/",
        StrategyDeleteView.as_view(),
        name="strategy-delete",
    ),
    path(
        "instruments/",
        generic.ListView.as_view(
            model=Instrument, template_name="backtester/instruments.html"
        ),
        name="instruments",
    ),
    path(
        "instruemnt/<int:pk>/",
        InstrumentDetailView.as_view(),
        name="instrument-detail",
    ),
]
