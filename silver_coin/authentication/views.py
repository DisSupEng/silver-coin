from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.urls import reverse

from .forms import SignupForm

class CustomLoginView(LoginView):
    """
    A class that is used to redirect users if they are already logged in
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return super().get(request, *args, **kwargs)

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