from django.urls import path, include
from django.contrib.auth.views import LoginView

from .views import IndexView

urlpatterns = [
    # The index page
    path("", IndexView.as_view(), name="index"),
    path("login/", LoginView(template_name="login.html").as_view()),
    path("signup/")
]