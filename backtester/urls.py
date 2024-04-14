from django.urls import path

from .views import *

app_name = "backtester"
urlpatterns = [
    path("", IndexListView.as_view(), name="index-list"),
    path("detail/<int:pk>/", DetailView.as_view(), name="detail"),
    path("result/<int:pk>/", ResultView.as_view(), name="result"),
    path("strategy/add/", StrategyCreateView.as_view(), name="strategy-add"),
    path("strategy/<int:pk>/delete/", StrategyDeleteView.as_view(), name="strategy-delete"),
]