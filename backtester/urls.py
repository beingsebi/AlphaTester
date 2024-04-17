from django.urls import path

from .views import IndexListView, DetailView, ResultView, StrategyCreateView, StrategyDeleteView

# ! Constant name "app_name" doesn't conform to UPPER_CASE naming stylePylintC0103:invalid-name
app_name = "backtester"  # ? Is this necessary?

urlpatterns = [
    path("", IndexListView.as_view(), name="index-list"),
    path("detail/<int:pk>/", DetailView.as_view(), name="detail"),
    path("result/<int:pk>/", ResultView.as_view(), name="result"),
    path("strategy/add/", StrategyCreateView.as_view(), name="strategy-add"),
    path("strategy/<int:pk>/delete/",
         StrategyDeleteView.as_view(), name="strategy-delete"),
]
