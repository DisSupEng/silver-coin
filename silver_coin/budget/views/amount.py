from typing import Any, Dict
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpResponseNotFound
from django.views.generic import ListView
from django.views.generic import FormView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from ..forms import AmountForm
from ..forms import IncomeForm
from ..forms import ActualAmountForm
from ..models import Budget
from ..models import BudgetPeriod
from ..models import Amount
from ..models import ActualAmount

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
    
class ActualAmountList(LoginRequiredMixin, ListView):
    """
    A view for displaying Actual Amounts.
    """
    model = ActualAmount
    template_name = "amount/actual_amount_list.html"
    context_object_name = "actual_amounts"

    def get_login_url(self):
        return reverse("login")
    
    def get_context_data(self, **kwargs):
        """
        Override to get the incomes and expenses as separate querysets.
        """
        actual_amounts = self.get_queryset()
        actual_incomes = actual_amounts.filter(estimate__amount_type="IN")
        total_income = sum([income.amount for income in actual_incomes])
        actual_expenses = actual_amounts.filter(estimate__amount_type="EX")
        total_expense = sum([expense.amount for expense in actual_expenses])
        return super().get_context_data(
            **kwargs,
            period_id=self.kwargs["period_id"], 
            incomes=actual_incomes, 
            expenses=actual_expenses, 
            total_income=total_income, 
            total_expense=total_expense,
            net_amount=total_expense - total_income,
        )
    
    def get(self, request, *args, **kwargs):
        """
        Override to make sure the user owns the budget.
        """
        try:
            owner = BudgetPeriod.objects.get(budget_period_id=kwargs["period_id"]).budget.owner
            if owner == request.user:
                return super().get(request, *args, **kwargs)
            else:
                return HttpResponseNotFound()
        except BudgetPeriod.DoesNotExist:
            return HttpResponseNotFound()
    
    def get_queryset(self):
        """
        Override to get the actual amounts for this budget period
        """
        period_id = self.kwargs["period_id"]

        return ActualAmount.objects.filter(period_id=period_id)
    
class CreateActualIncome(LoginRequiredMixin, FormView):
    """
    A view for creating an actual income.
    """
    form_class = ActualAmountForm
    template_name = "amount/actual_amount_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs,
            period_id=self.kwargs["period_id"],
            action="Create",
            type="Income"
        )

        form = context["form"]
        incomes = Amount.objects.filter(budget_period=self.kwargs["period_id"], amount_type="IN")
        choices = []
        for income in incomes:
            choices.append(
                (income.amount_id, f"{income.name} - ${income.amount}")
            )

        
        
        form.fields["estimate"].choices = choices

        return context
        


    def get_login_url(self):
        return reverse("login")
    
    def post(self, request, *args, **kwargs):
        """
        Override to add extra fields to the model.
        """
        budget_period = BudgetPeriod.objects.get(budget_period_id=kwargs["period_id"])
        form = self.form_class(request.POST)

        if form.is_valid():
            actual_amount = ActualAmount(
                **form.cleaned_data,
                period=budget_period
            )
            try:
                actual_amount.full_clean()
            except ValidationError as error:
                form.add_error(error=error.message)
                return self.form_invalid(form)
            actual_amount.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
