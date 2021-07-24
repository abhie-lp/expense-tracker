"""URL routes for user application"""

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import register_view

app_name = "users"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]
