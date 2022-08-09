from django.views.generic import TemplateView, FormView
from django.urls import reverse

from .forms import SignupForm

class SignUpView(FormView):
    template_name = "signup.html"
    form_class = SignupForm
    
    def get_success_url(self):
        return reverse("signup")

class IndexView(TemplateView):
    template_name = "index.html"