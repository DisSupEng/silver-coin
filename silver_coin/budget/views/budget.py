from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import FormView

from budget.forms import BudgetForm
from budget.models import Budget

class CreateBudget(FormView):
    form_class = BudgetForm
    template_name = "budget/budget_form.html"
    success_url = reverse_lazy("dashboard")

    def post(self, request, *args, **kwargs):
        owner = request.user
        form = self.form_class(request.POST)

        if form.is_valid():
            budget = Budget(**form.cleaned_data, owner=owner)
            try:
                budget.full_clean()
            except ValidationError as error:
                form.add_error(error=error.message)
                return self.form_invalid(form)
            budget.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
