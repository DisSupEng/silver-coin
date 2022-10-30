from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from formtools.wizard.views import SessionWizardView

from ..models import Budget, Amount
from ..forms import AmountForm, BudgetForm

class BudgetWizard(SessionWizardView):
    form_list = [
        ("Budget", BudgetForm),
        ("Incomes", modelformset_factory(Amount, form=AmountForm, min_num=1, validate_min=True)),
        ("Expenses", modelformset_factory(Amount, form=AmountForm, min_num=1, validate_min=True))
    ]
    template_name = "budget/policy_wizard.html"

    def done(self, form_list, form_dict, **kwargs):
        processed_budget_form: BudgetForm = self.processed_budget_form(form_dict["budget"])
        processed_budget_form.instance
    
        processed_budget_form.full_clean()
        if processed_budget_form.is_valid():
            processed_budget_form.save()

            # Process the income and expenses forms
            processed_income_form: AmountForm = self.process_amount_form(form_dict["income"], processed_budget_form.instance, True)
            processed_income_form.full_clean()

            processed_expense_form: AmountForm = self.process_amount_form(form_dict["expense"], processed_budget_form.instance, False)
            processed_expense_form.full_clean()

            # All forms are valid redirect back to the dashboard
            if processed_income_form.is_valid() and processed_expense_form.is_valid():
                processed_income_form.save()
                processed_expense_form.save()
                return redirect(reverse("dashboard"))
            # At least one of the amount forms is not valid
            else:
                errors = {}
                if processed_income_form.is_valid() == False:
                    errors["income_errors"] = processed_income_form.errors
                if processed_expense_form.is_valid() == False:
                    errors["expense_errors"] = processed_expense_form.errors

                return render(
                    self.request,
                    "budget_wizard.html",
                    {
                        "form_data": [form.cleaned_data for form in form_list],
                        "form_errors": errors
                    }
                )


        # Has errors render the budget wizard again with the errors from the budget form
        else:
            return render(
                self.request, 
                "budget_wizard.html",
                {
                    "form_data": [form.cleaned_data for form in form_list],
                    "form_errors": {"budget_errors": processed_budget_form.errors}
                }
            )

        return super().done(form_list, **kwargs)

    
    def process_budget_form(self, budget_form: BudgetForm) -> BudgetForm:
        """
        Adds the other fields to the budget form and returns the modified form.

        :param: budget_form, the form for the budget

        :returns: BudgetForm, the modified budget form with additional fields
        """
        # Add the owner to the fields
        budget_form.fields["owner"] = self.request.user
        return budget_form

    def process_amount_form(self, amount_form: AmountForm, budget: Budget, is_income: bool) -> AmountForm:
        """
        Adds the other required fields to the income form and returns the modified form.

        :param: amount_form, the form for an income or expense
        :param: budget, the budget that the amount should be attached to
        :param: is_income, whether the amount is an income or not

        :returns: AmountForm, the modified form with extra fields
        """
        # TODO: modify method to use formset instead of a single form.
        # If the form is for incomes 
        if is_income:
            amount_form.fields["amount_type"] = "IN"
        # If the form is for expenses
        else:
            amount_form.fields["amount_type"] = "EX"

        amount_form.fields["is_actual"] = False
        amount_form.fields["is_one_time_cost"] = False
        amount_form.fields["budget"] = budget
        amount_form.fields["owner"] = self.request.user

        return amount_form
