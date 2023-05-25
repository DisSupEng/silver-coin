from django.urls import path

from .views import IndexView
from .views import SignUpView
from .views import CustomLoginView

urlpatterns = [
    # The index page
    path("", IndexView.as_view(), name="index"),
    path("login/", CustomLoginView.as_view(template_name="login.html"), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
]