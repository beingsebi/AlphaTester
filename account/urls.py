from django.urls import path  # type: ignore

# from . import views
# from django.contrib import admin
from django.contrib.auth import views as auth_views  # type: ignore
from .views import SignUpView, index

urlpatterns = [
    path("", index, name="index"),
    path("register/", SignUpView.as_view(), name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="account/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
