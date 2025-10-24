from datetime import datetime

from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models

from budget.models import Budget, BudgetPeriod

class Goal(models.Model):
    """
    A Goal is linked to a User and is used to track the money that the user has set
    aside for a particular purpose.

    The model contains the following fields:
    * name: The name of the Goal
    * amount: The total cost of this Goal
    * expected_contribution: The amount expected to be saved each BudgetPeriod
    * budget: The budget that the goal is attached to
    * owner: The user that this Goal belongs to
    """
    goal_id = models.AutoField(primary_key=True)
    name = models.CharField(
        validators=[MaxLengthValidator(50, "Name cannot be greater than 50 characters")],
        max_length=50,
        null=False,
        blank=False
    )
    amount = models.DecimalField(
        validators=[MinValueValidator(1, "Amount must be greater than zero")],
        max_digits=7,
        decimal_places=2,
        null=False,
        blank=False
    )
    expected_contribution = models.DecimalField(
        validators=[MinValueValidator(1, "Expected contribution must be greater than zero")],
        max_digits=7,
        decimal_places=2,
        null=False,
        blank=False
    )
    budget = models.ForeignKey(Budget, related_name="goals", on_delete=models.CASCADE, null=False, blank=False)

    @property
    def savings(self) -> float:
        """
        Returns the total amount that has been saved for this goal
        """
        return sum([contribution.amount for contribution in self.contributions.all()])

    @property
    def is_complete(self) -> bool:
        """
        Returns True if the savings is greater than or equal to the amount.
        """
        return self.savings >= self.amount

    @property
    def income_percentage(self) -> float:
        """
        The percentage of the income that the Goal contribution takes up.
        """
        income = self.budget.total_income()
        if income != 0:
            percentage = (self.expected_contribution / income) * 100
            return "{:0.2f}".format(percentage)
        else:
            return "N/A"

    def full_clean(self, *args, **kwargs):
        """
        Check that the dollar amounts cannot be less than zero.
        """
        super().full_clean(*args, **kwargs)

        if self.amount <= 0:
            raise ValidationError("Amount cannot be less than or equal to zero")
        if self.expected_contribution <= 0:
            raise ValidationError("Expected Contribution cannot be less than or equal to zero")

class Contribution(models.Model):
    """
    A Contribution is linked to a particular Goal and contains the following fields:
    * amount: The amount that is being contributed to the Goal
    * goal: The goal that this Contribution is linked to
    * budget_period: The BudgetPeriod that this Contribution is linked to
    """
    contribution_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(
        validators=[MinValueValidator(0.1, "Amount must be greater than or equal to 0.1")],
        max_digits=7,
        decimal_places=2,
        null=False,
        blank=False
    )
    occurred_on = models.DateField(null=False, blank=False, default=datetime.now)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=False, blank=False, related_name="contributions")
    budget_period = models.ForeignKey(BudgetPeriod, on_delete=models.CASCADE, null=False, blank=False)

    def full_clean(self, *args, **kwargs):
        """
        A Contribution must occur within the dates for the BudgetPeriod.
        """
        super().full_clean(*args, **kwargs)

        start_date = self.budget_period.start_date
        end_date = self.budget_period.end_date
        
        if self.occurred_on < start_date:
            raise ValidationError("Occurred On must be greater than or equal to period start date")
        elif self.occurred_on > end_date:
            raise ValidationError("Occurred On must be less than or equal to the end date")
