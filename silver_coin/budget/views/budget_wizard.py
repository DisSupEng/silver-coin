from formtools.wizard.views import SessionWizardView

from ..forms import AmountForm, BudgetForm

class BudgetWizard(SessionWizardView):
    form_list = [
        ("Budget", BudgetForm),
        ("Incomes", AmountForm),
        ("Expenses", AmountForm)
    ]

    def done(self, form_list, **kwargs):
        return super().done(form_list, **kwargs)