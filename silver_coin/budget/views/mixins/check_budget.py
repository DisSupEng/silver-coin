from django.shortcuts import redirect
from django.urls import reverse

from budget.models import Budget

class CheckBudgetExists:
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