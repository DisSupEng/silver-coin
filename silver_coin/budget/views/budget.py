from typing import Any, Optional
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView

from budget.forms import BudgetForm
from budget.models import Budget

class CreateBudget(FormView):
    """
    A FormView that is used to create a budget. This needs to be a FormView because we need to add the logged in user as the owner.
    A ModelForm will not work because the form will not be valid without an owner and adding the owner to get_form_kwargs cannot be done as it is immutable.
    We therefore validate what we can using the FormView, create the Budget instance and add the owner to that.
    """
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

class EditBudget(DetailView):
    """
    A view for editing the Budget instance.
    """
    model = Budget
    template_name = "budget/budget_form.html"

    def get_queryset(self):
        """
        Override to filter by the owner.
        """
        queryset = Budget.objects.filter(owner=self.request.user)
        return queryset
    
    def get_object(self):
        return self.get_queryset().first()