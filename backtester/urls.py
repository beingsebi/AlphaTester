from django.urls import path
from django.views import generic

from .models import Instrument
from .views import *

app_name = "backtester"
#  because it is needed by Django

urlpatterns = [
    path("", StrategyListView.as_view(), name="index-list"),
    path("detail/<int:pk>/", StrategyDetailView.as_view(), name="detail"),
    path("strategy/add/", StrategyCreateView.as_view(), name="strategy-add"),
    path(
        "strategy/<int:pk>/delete/",
        StrategyDeleteView.as_view(),
        name="strategy-delete",
    ),
    path(
        "strategy/<int:pk>/update/",
        UpdateStrategy.as_view(),
        name="strategy-update",
    ),
    path(
        "instruments/",
        generic.ListView.as_view(model=Instrument,
                                 template_name="backtester/instruments.html"),
        name="instruments",
    ),
    path(
        "instruemnt/<int:pk>/",
        InstrumentDetailView.as_view(),
        name="instrument-detail",
    ),
]
