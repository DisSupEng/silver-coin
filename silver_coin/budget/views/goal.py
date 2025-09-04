from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView

from budget.forms import GoalForm
from budget.models import Budget, Goal
from budget.views.mixins import CheckBudgetExists, CheckGoalOwner


class CreateGoal(LoginRequiredMixin, CheckBudgetExists, FormView):
    """
    The view that handles the logic for creating Goals.
    """
    form_class = GoalForm
    template_name = "goal/goal_form.html"
    success_url = reverse_lazy("amount")
    extra_context = {"action": "Create", "type": "Goal"}

    def post(self, request):
        """
        When a Goal is created we need to get the Budget from the current user.
        """
        budget = Budget.objects.get(owner=request.user)
        form = self.form_class(request.POST)

        if form.is_valid():
            goal = Goal(**form.cleaned_data, budget=budget)
            try:
                goal.full_clean()
            except ValidationError as error:
                form.add_error(error=error)
                return self.form_invalid(form)
            goal.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class EditGoal(LoginRequiredMixin, CheckGoalOwner, UpdateView):
    """
    The view that handles the logic for editing Goals.
    """
    model = Goal
    form_class = GoalForm
    success_url = reverse_lazy("amount")
    template_name = "goal/goal_form.html"
    extra_context = {"action": "Edit", "type": "Goal"}

    def get_queryset(self):
        """
        Get the queryset for the Budget's goals.
        """
        budget = Budget.objects.get(owner=self.request.user)
        return Goal.objects.filter(budget=budget)

    def get_login_url(self):
        return reverse("login")
