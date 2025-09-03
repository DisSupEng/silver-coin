from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from budget.forms import GoalForm
from budget.views.mixins import CheckBudgetExists


class CreateGoal(LoginRequiredMixin, CheckBudgetExists, FormView):
    """
    The view that handles the logic for creating Goals.
    """
    form_class = GoalForm
    template_name = "goal/goal_form.html"
    success_url = reverse_lazy("amount")
    extra_context = {"action": "Create", "type": "Goal"}
