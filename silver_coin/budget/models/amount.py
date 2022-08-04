from re import U
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from .budget import Budget

class Amount(models.Model):
    """
    An Amount represents an estimate expense/income or an actual expense/income.
    An Amount may be linked to either a Budget or BudgetPeriod but not both.
    If linked to a Budget then it is an estimate.
    If linked to a BudgetPeriod then it is an actual.
    """
    AMOUNT_TYPES = [
        ("IN", "Income"),
        ("EX", "Expenses"),
    ]

    amount_id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, blank=False, max_length=2, verbose_name="Name")
    amount_type = models.CharField(choices=AMOUNT_TYPES, null=False, blank=False, max_length=2, verbose_name="Type")
    # The maximum number of digits including decimal places is 7
    amount = models.DecimalField(null=False, blank=False, max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01, "Amount must be positive, mark as Expense if outgoing cost")])
    budget = models.ForeignKey(Budget, null=True, blank=True, db_column="budget", on_delete=models.CASCADE, verbose_name="Budget")
    # An Amount should be linked to the User
    owner = models.ForeignKey(User, null=False, blank=True, editable=False, db_column="owner", on_delete=models.CASCADE)