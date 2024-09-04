from typing import Any, Dict
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy

from ..forms import BudgetPeriodForm, BudgetPeriodModelForm
from ..models import BudgetPeriod, Budget

class BudgetPeriodList(ListView):
    """
    Lists the BudgetPeriod for the user's Budget.
    """
    model = BudgetPeriod
    template_name = "budget_period/budget_period_list.html"
    context_object_name = "budget_periods"

    def get_login_url(self):
        return reverse("login")
    
    def get_queryset(self):
        """
        Override to get the budget periods
        """
        budget_periods = BudgetPeriod.objects.filter(budget__owner=self.request.user).order_by("-start_date")
        return budget_periods

class CreateBudgetPeriod(LoginRequiredMixin, FormView):
    """
    Creates a BudgetPeriod
    """
    form_class = BudgetPeriodForm
    template_name = "budget_period/budget_period_form.html"
    success_url = reverse_lazy("budget_period")
    extra_context = {"action": "Create"}

    def post(self, request, *args, **kwargs):
        owner = request.user
        form = self.form_class(request.POST)

        if form.is_valid():
            budget = Budget.objects.get(owner=owner)
            budget_period = BudgetPeriod(**form.cleaned_data, budget=budget)
            try:
                budget_period.full_clean()
            except ValidationError as error:
                form.add_error(field=None, error=error)
                return self.form_invalid(form)
            budget_period.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class EditBudgetPeriod(UpdateView):
    """
    A view for editing the user's budget period.
    """
    form_class = BudgetPeriodModelForm
    template_name = "budget_period/budget_period_form.html"
    success_url = reverse_lazy("budget_period")
    model = BudgetPeriod
    context_object_name = "budget_period"
    extra_context = {"action": "Edit"}
        
class DeleteBudgetPeriod(DeleteView):
    """
    A view for deleting the user's budget period.
    """
    template_name = "budget_period/budget_period_delete.html"
    success_url = reverse_lazy("budget_period")
    model = BudgetPeriod
    context_object_name = "budget_period"