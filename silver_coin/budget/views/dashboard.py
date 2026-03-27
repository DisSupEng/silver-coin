from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse

from ..models import Budget, BudgetPeriod

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        has_budget = Budget.objects.filter(owner=self.request.user).count() > 0
        last_period = BudgetPeriod.objects.filter(budget__owner=self.request.user).last()

        recent_net_amount = last_period.net_amount() if last_period else None

        return super().get_context_data(
            **kwargs,
            has_budget=has_budget,
            recent_net_amount=recent_net_amount,
            page_title="Dasboard"
        )

    def get_login_url(self):
        """
        Override to use reverse. Reverse cannot be used if you try to override the login_url class property.
        """
        return reverse("login")


