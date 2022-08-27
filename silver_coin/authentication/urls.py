from django.urls import path, include
from django.contrib.auth.views import LoginView

from .views import IndexView, SignUpView

urlpatterns = [
    # The index page
    path("", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
]