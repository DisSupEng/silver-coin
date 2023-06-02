from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.views.generic import ListView
from django.views.generic import FormView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse, reverse_lazy

from ..forms import AmountForm
from ..forms import IncomeForm
from ..models import Budget
from ..models import Amount

class AmountList(LoginRequiredMixin, ListView):
    """
    Displays the Incomes and Expenses.
    """
    model = Amount
    template_name = "amount/amount_list.html"
    context_object_name = "amounts"
    
    def get_login_url(self):
        return reverse("login")

    def get_queryset(self):
        """
        Override to get the amounts for the budget.
        """
        amounts = Budget.objects.get(owner=self.request.user).amounts
        return amounts
    
    def get_context_data(self, **kwargs):
        """
        Override to get the incomes and expenses as separate querysets.
        """
        amounts = self.get_queryset()
        incomes = amounts.filter(amount_type="IN")
        total_income = sum([income.amount for income in incomes])
        expenses = amounts.filter(amount_type="EX")
        total_expense = sum([expense.amount for expense in expenses])
        return super().get_context_data(
            **kwargs, 
            incomes=incomes, 
            expenses=expenses, 
            total_income=total_income, 
            total_expense=total_expense,
            net_amount=Budget.objects.get(owner=self.request.user).net_amount()
        )
    
class CreateIncome(LoginRequiredMixin, FormView):
    """
    A view for creating Incomes
    """
    form_class = AmountForm
    success_url = reverse_lazy("amount")
    template_name = "amount/income_form.html"
    extra_context = {"action": "Create", "type": "Income"}

    def get_login_url(self):
        return reverse("login")
    
    def post(self, request, *args, **kwargs):
        """
        Override to add extra fields to the model.
        """
        budget = Budget.objects.get(owner=request.user)
        form = self.form_class(request.POST)

        if form.is_valid():
            amount = Amount(
                **form.cleaned_data,
                amount_type="IN",
                is_actual=False,
                is_one_time_cost=False,
                budget=budget
            )
            try:
                amount.full_clean()
            except ValidationError as error:
                form.add_error(error=error.message)
                return self.form_invalid(form)
            amount.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class EditIncome(LoginRequiredMixin, UpdateView):
    """
    A view for editing an income.
    """
    model = Amount
    form_class = IncomeForm
    success_url = reverse_lazy("amount")
    template_name = "amount/income_form.html"
    extra_context = {"action": "Edit", "type": "Income"}

    def get(self, request, *args, **kwargs):
        """
        Make sure the user owns this amount before proceeding.
        """
        try:
            amount = Amount.objects.get(pk=request.GET.get("pk"))
            # If the user does not own the amount return a not found
            if amount.budget.owner != request.user:
                return HttpResponseNotFound()
        except Amount.DoesNotExist:
            return HttpResponseNotFound()
        # The user is the owner
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Get the queryset for the Budget's incomes.
        """
        budget = Budget.objects.get(owner=self.request.user)
        incomes = Amount.objects.filter(amount_type="IN", budget=budget)
        return incomes

    def get_login_url(self):
        return reverse("login")

class DeleteIncome(LoginRequiredMixin, DeleteView):
    """"
    A view for deleting an income.
    """
    model = Amount
    success_url = reverse_lazy("amount")
    template_name = "amount/amount_delete.html"
    extra_context = {"type": "Income"}
    
    def get_queryset(self):
        """
        Get the queryset for the Budget's incomes.
        """
        budget = Budget.objects.get(owner=self.request.user)
        incomes = Amount.objects.filter(amount_type="IN", budget=budget)
        return incomes
    
class CreateExpense(LoginRequiredMixin, FormView):
    """
    A view for creating Expenses
    """
    form_class = AmountForm
    success_url = reverse_lazy("amount")
    template_name = "amount/expense_form.html"
    extra_context = {"action": "Create", "type": "Expense"}

    def get_login_url(self):
        return reverse("login")
    
    def post(self, request, *args, **kwargs):
        """
        Override to add extra fields to the model.
        """
        budget = Budget.objects.get(owner=request.user)
        form = self.form_class(request.POST)

        if form.is_valid():
            amount = Amount(
                **form.cleaned_data,
                amount_type="EX",
                is_actual=False,
                is_one_time_cost=False,
                budget=budget
            )
            try:
                amount.full_clean()
            except ValidationError as error:
                form.add_error(error=error.message)
                return self.form_invalid(form)
            amount.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class EditExpense(LoginRequiredMixin, UpdateView):
    """
    A view for editing an expense
    """
    model = Amount
    form_class = IncomeForm
    success_url = reverse_lazy("amount")
    template_name = "amount/expense_form.html"
    extra_context = {"action": "Edit", "type": "Expense"}

    def get_queryset(self):
        """
        Get the queryset for the Budget's expense.
        """
        budget = Budget.objects.get(owner=self.request.user)
        incomes = Amount.objects.filter(amount_type="EX", budget=budget)
        return incomes

    def get_login_url(self):
        return reverse("login")

class DeleteExpense(LoginRequiredMixin, DeleteView):
    """"
    A view for deleting an expense.
    """
    model = Amount
    success_url = reverse_lazy("amount")
    template_name = "amount/amount_delete.html"
    extra_context = {"type": "Expense"}
    
    def get_queryset(self):
        """
        Get the queryset for the Budget's expense
        """
        budget = Budget.objects.get(owner=self.request.user)
        incomes = Amount.objects.filter(amount_type="EX", budget=budget)
        return incomes


    def get_login_url(self):
        return reverse("login")