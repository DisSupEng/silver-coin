from django.views.generic import ListView

from ..models import Budget
from ..models import Amount

class AmountList(ListView):
    model = Amount
    template_name = "amount/amount_list.html"
    context_object_name = "amounts"
    

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
        expenses = amounts.filter(amount_type="EX")
        return super().get_context_data(**kwargs, incomes=incomes, expenses=expenses)
