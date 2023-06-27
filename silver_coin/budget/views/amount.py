from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.views.generic import ListView
from django.views.generic import FormView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

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
    
class CheckBudgetExists():
    """
    A Mixin that checks if the user has a Budget.

    Will redirect to the dashboard if they don't.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Override to check the user has a Budget.
        """
        try:
            Budget.objects.get(owner=request.user)
        except Budget.DoesNotExist:
            return redirect(reverse("dashboard"))

        return super().dispatch(request, *args, **kwargs)
    
class CreateIncome(LoginRequiredMixin, CheckBudgetExists, FormView):
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
        
class CheckOwner():
    """
    A mixin that checks whether the owner of the amount is the same as the user performing the request.
    """

    """
    Adds a check at the start of the get request to check the owner.
    Also checks that the user actually has a budget of their own.0
    """
    def check_owner(self, amount_id, user):
        """
        Checks that the user is the owner of the amount they are trying to access.

        :param: amount_id, the id of the amount object
        :param: user, the user making the request

        :returns: True if owner, 302 if they do not have a budget, 404 if they are trying to aceess an amount that is not theirs
        """
        # If the user does not have a budget redirect to dashboard
        try:
            Budget.objects.get(owner=user)
        except Budget.DoesNotExist:
            return redirect(reverse("dashboard"))
        try:
            amount = Amount.objects.get(pk=amount_id)
            if amount.budget.owner != user:
                return HttpResponseNotFound()
        except Amount.DoesNotExist:
            return HttpResponseNotFound()
        # They have a budget and they are the owner
        return True

    def get(self, request, *args, **kwargs):
        """
        Override to check the owner and redirect if required.
        """
        owner_response = self.check_owner(kwargs["pk"], request.user)
        if owner_response is not True:
            # Is a redirect or 404
            return owner_response
        # Owner OK, continue
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """
        Override to check the owner and redirect if required.
        """
        owner_response = self.check_owner(kwargs["pk"], request.user)
        if owner_response is not True:
            # Is a redirect or 404
            return owner_response
        # Owner OK, continue
        return super().post(request, *args, **kwargs)
        
        
class EditIncome(CheckOwner, LoginRequiredMixin, UpdateView):
    """
    A view for editing an income.
    """
    model = Amount
    form_class = IncomeForm
    success_url = reverse_lazy("amount")
    template_name = "amount/income_form.html"
    extra_context = {"action": "Edit", "type": "Income"}

    def get_queryset(self):
        """
        Get the queryset for the Budget's incomes.
        """
        budget = Budget.objects.get(owner=self.request.user)
        incomes = Amount.objects.filter(amount_type="IN", budget=budget)
        return incomes

    def get_login_url(self):
        return reverse("login")

class DeleteIncome(CheckOwner, LoginRequiredMixin, DeleteView):
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
    
class CreateExpense(LoginRequiredMixin, CheckBudgetExists, FormView):
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
        
class EditExpense(CheckOwner, LoginRequiredMixin, UpdateView):
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