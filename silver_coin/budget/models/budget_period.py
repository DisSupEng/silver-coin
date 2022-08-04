from django.db import models
from django.utils import timezone

from .budget import Budget

class BudgetPeriod(models.Model):
    
    budget_period_id = models.AutoField(primary_key=True)
    start_date = models.DateField(null=False, blank=False, default=timezone.now, verbose_name="Start Date")
    # This is not editable because it is determined by the Budget object it is linked to
    end_date = models.DateField(null=False, blank=False, editable=False, verbose_name="End Date")
    # Actual Expenses are defined on the Amount model
    # Actual Incomes are defined on the Amount model
    budget = models.ForeignKey(Budget, null=False, blank=False, db_column="budget", on_delete=models.CASCADE, verbose_name="Budget")
