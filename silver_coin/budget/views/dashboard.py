from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse

from ..forms import BudgetForm, AmountForm
from ..models import Budget

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        """
        Override to check if the user has a budget defined.
        """
        has_budget = Budget.objects.filter(owner=request.user).count() > 0

        return super().get(request, has_budget=has_budget)

    def get_login_url(self):
        """
        Override to use reverse. Reverse cannot be used if you try to override the login_url class property.
        """
        return reverse("login")


