from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from budget.forms import BudgetForm
from budget.forms import BudgetModelForm
from budget.models import Budget

class CreateBudget(LoginRequiredMixin, FormView):
    """
    A FormView that is used to create a budget. This needs to be a FormView because we need to add the logged in user as the owner.
    A ModelForm will not work because the form will not be valid without an owner and adding the owner to get_form_kwargs cannot be done as it is immutable.
    We therefore validate what we can using the FormView, create the Budget instance and add the owner to that.
    """
    form_class = BudgetForm
    template_name = "budget/budget_form.html"
    success_url = reverse_lazy("dashboard")
    extra_context = {"action": "Create"}

    def get_login_url(self):
        return reverse("login")

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
        
class UserMixin(LoginRequiredMixin):
    """
    A mixin to get the budget for the logged in user.
    """
    def get_login_url(self):
        return reverse("login")

    def get_queryset(self):
        """
        Override to filter by the owner.
        """
        queryset = Budget.objects.filter(owner=self.request.user)
        return queryset
    
    def get_object(self):
        """
        Return the user's budget.
        """
        return self.get_queryset().first()

class EditBudget(UserMixin, UpdateView):
    """
    A view for editing the Budget instance.
    """
    form_class = BudgetModelForm
    template_name = "budget/budget_form.html"
    success_url = reverse_lazy("dashboard")
    extra_context = {"action": "Edit"}

    
    
class DeleteBudget(UserMixin, DeleteView):
    """
    A view for deleting the user's budget.
    """
    template_name = "budget/budget_delete.html"
    success_url = reverse_lazy("dashboard")
