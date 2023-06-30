from django.db import models

from datetime import datetime
from django.core.exceptions import ValidationError

class AmountManager(models.Manager):
    def create_amount(self, amount, period):
        """ 
        This method will be called when creating a new BudgetPeriod.
        The Amount objects on the Budget must be copied so they are recorded as they were at the time 
        (remember Budget objects can change and historical data should remain unchanged).

        The name, amount_type and amount will be copied and the parent will be assigned to either the
        budget or budget_period depending on the type of the parent.
        """
        # Link it to a Budget Period
        self.create(
            name=amount.name, 
            amount_type=amount.amount_type, 
            amount=amount.amount,
            budget_period=period,
        )

class Amount(models.Model):
    """
    An Amount represents an estimate expense/income or an actual expense/income.
    An Amount may be linked to either a Budget or BudgetPeriod but not both.
    If linked to a Budget then it is an estimate.
    If linked to a BudgetPeriod then it is an estimate or actual
    """
    AMOUNT_TYPES = [
        ("IN", "Income"),
        ("EX", "Expenses"),
    ]

    amount_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Name")
    amount_type = models.CharField(choices=AMOUNT_TYPES, null=False, blank=False, max_length=2, verbose_name="Type")
    # The maximum number of digits including decimal places is 7
    amount = models.DecimalField(null=False, blank=False, max_digits=7, decimal_places=2)
    budget = models.ForeignKey("Budget", null=True, blank=True, default=None, db_column="budget", on_delete=models.CASCADE, verbose_name="Budget", related_name="amounts")
    budget_period = models.ForeignKey("BudgetPeriod", null=True, blank=True, default=None, db_column="budget_period", on_delete=models.CASCADE, verbose_name="Budget Period")

    # Define the model manager
    objects = AmountManager()


    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        """
        An Amount must be linked to either a Budget or Budget Period but not both.
        Amount must be greater than zero
        One time amounts can only be linked to a Budget Period
        """
        super().full_clean()

        if self.budget is None and self.budget_period is None:
            raise ValidationError("An Amount must be linked to either a Budget or BudgetPeriod")
        elif self.budget is not None and self.budget_period is not None:
            raise ValidationError("An Amount cannot be linked to both a Budget and BudgetPeriod")

        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero, mark as expense if outgoing cost")
        
    @property
    def income_percentage(self):
        """
        Returns the percentage of the income the amount is rounded to 2dp.
        """
        income = self.budget.total_income()
        percentage = (self.amount / income) * 100

        return "{:0.2f}".format(percentage)
    
class ActualAmount(models.Model):
    """
    An ActualAmount is the model that represents what a user actually spends.

    It is linked to an Amount which determines the type of Amount it is, i.e name and type.
    It is also linked to a BudgetPeriod which records how much was actually spend over the period of time.
    """
    actual_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    occurred_on = models.DateField(null=False, blank=False, default=datetime.now)
    amount = models.DecimalField(null=False, blank=False, max_digits=7, decimal_places=2)
    estimate = models.ForeignKey("Amount", null=False, on_delete=models.CASCADE, related_name="actual_amounts")
    period = models.ForeignKey("BudgetPeriod", null=False, on_delete=models.CASCADE, related_name="amounts")

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True) -> None:
        super().full_clean()

        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero")
        
        if self.occurred_on >= self.period.start_date:
            raise ValidationError("Occurred On must be greater than or equal to period start date")
        elif self.occurred_on < self.period.end_date:
            raise ValidationError("Occurred On must be less than end date")