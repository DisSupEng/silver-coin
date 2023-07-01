from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
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

    def full_clean(self, exclude=None, validate_unique=True):
        super().full_clean(exclude=["end_date"])
        end_date = self.calculate_end_date()

        # If we are editing an existing period exclude the current model instance
        if self.budget_period_id:
            # Once the dates are calculated, double check that there are no overlapping periods
            overlapping_count = BudgetPeriod.objects.filter(
                ~Q(budget_period_id=self.budget_period_id),
                Q(start_date__lte=self.start_date, end_date__gt=self.start_date) |
                Q(start_date__lte=end_date, end_date__gt=end_date)
            ).count()
        else:
            # Once the dates are calculated, double check that there are no overlapping periods
            overlapping_count = BudgetPeriod.objects.filter(
                Q(start_date__lte=self.start_date, end_date__gt=self.start_date) |
                Q(start_date__lte=end_date, end_date__gt=end_date)
            ).count()
        if overlapping_count > 0:
            raise ValidationError("Budget Period overlaps with existing period, please check the dates and try again!")
        
        return None

    def save(self, *args, **kwargs):
        self.end_date = self.calculate_end_date()

        # Only create amounts if it is the first time saving
        if self._state.adding:
            super().save(*args, **kwargs)

            # Create the Incomes and Expense for this Budget Period
            costs = Amount.objects.filter(budget=self.budget)
            for cost in costs.all():
                # Copy the estimates from the budget as they are currently
                Amount.objects.create_amount(cost, self)
            
            return None
        else:
            return super().save(*args, **kwargs)
        
    def calculate_end_date(self):
        """
        Method calculates when the end date of the BudgetPeriod will be.
        """
        period_length = self.budget.period_length
        start_datetime = datetime.combine(self.start_date, datetime.min.time())
        end_date = None

        if self.budget.period_type == DAYS:
            end_date = (start_datetime + relativedelta(days=period_length)).date()
        elif self.budget.period_type == WEEKS:
            end_date = (start_datetime + relativedelta(weeks=period_length)).date()
        else:
            end_date = (start_datetime + relativedelta(months=period_length)).date()

        return end_date

    def is_ended(self):
        """
        Returns if the Budget period has ended.
        """
        return self.end_date < timezone.now().date()