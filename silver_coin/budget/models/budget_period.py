from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from ..helpers import DAYS, WEEKS, MONTHS, YEARS

from ..models import Amount

class BudgetPeriod(models.Model):
    """
    A Budget Period is based on a Budget object. The end date is calculated using the period type and length from the Budget and is not editable.
    The estimates should be copied from the Budget as well. This is because a Budget object can change and we want to keep a record of the estimates as they were at the
    time the Budget Period was created, otherwise the historical data might not make sense. 
    """
    budget_period_id = models.AutoField(primary_key=True)
    start_date = models.DateField(null=False, blank=False, default=timezone.now, verbose_name="Start Date")
    # This is not editable because it is determined by the Budget object it is linked to
    end_date = models.DateField(null=False, blank=False, editable=False, verbose_name="End Date")
    # Actual Expenses are defined on the Amount model
    # Actual Incomes are defined on the Amount model
    budget = models.ForeignKey("Budget", null=False, blank=False, db_column="budget", on_delete=models.CASCADE, verbose_name="Budget")

    def save(self, *args, **kwargs):
        period_length = self.budget.period_length
        start_datetime = datetime.combine(self.start_date, datetime.min.time())

        if self.budget.period_type == DAYS:
            self.end_date = (start_datetime + relativedelta(days=period_length)).date()
        elif self.budget.period_type == WEEKS:
            self.end_date = (start_datetime + relativedelta(weeks=period_length)).date()
        else:
            # Timedelta can't do months, calculate using weeks instead
            self.end_date = (start_datetime + relativedelta(months=period_length)).date()
        

        super().save(*args, **kwargs)

        # Create the Incomes and Expense for this Budget Period
        costs = Amount.objects.filter(budget=self.budget)
        for cost in costs:
            Amount.objects.create_amount(cost, self)

        return None

    def is_ended(self):
        """
        Returns if the Budget period has ended.
        """
        return self.end_date < timezone.now().date()