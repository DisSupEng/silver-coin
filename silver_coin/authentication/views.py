from urllib import request
from django.views.generic import TemplateView, FormView
from django.urls import reverse

from .forms import SignupForm

class IndexView(TemplateView):
    template_name = "index.html"

class SignUpView(FormView):
    template_name = "signup.html"
    form_class = SignupForm
    success_url = reverse("login")