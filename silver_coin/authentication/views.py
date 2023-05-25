from django.contrib.auth.hashers import make_password
from django.views.generic import TemplateView, FormView
from django.urls import reverse

from .forms import SignupForm

class SignUpView(FormView):
    template_name = "signup.html"
    form_class = SignupForm
    
    def get_success_url(self):
        """
        Redirect to the login screen.
        """
        return reverse("login")

    def form_valid(self, form):
        """
        If the form is valid then save the user.
        """
        user = form.save(commit=False)
        # Password has been confirmed to be valid
        user.password = make_password(form.cleaned_data["password"])
        # Save for real
        user.save()

        return super().form_valid(form)

class IndexView(TemplateView):
    template_name = "index.html"