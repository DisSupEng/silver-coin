from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User
from django.db import models

from budget.models import Budget

class Goal(models.Model):
    """
    A Goal is linked to a User and is used to track the money that the user has set
    aside for a particular purpose.

    The model contains the following fields:
    * name: The name of the Goal
    * savings: The current amount that has been saved for this Goal
    * amount: The total cost of this Goal
    * expected_contribution: The amount expected to be saved each BudgetPeriod
    * budget: The budget that the goal is attached to
    * owner: The user that this Goal belongs to
    """
    goal_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=50,
        validators=[MaxLengthValidator(50, "Name cannot be greater than 50 characters")],
        null=False,
        blank=False
    )
    savings = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    expected_contribution = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    @property
    def is_complete(self) -> bool:
        """
        Returns True if the savings is greater than or equal to the amount.
        """
        return self.savings >= self.amount

    def full_clean(self, *args, **kwargs):
        """
        Check that the dollar amounts cannot be less than zero.
        """
        super().full_clean(*args, **kwargs)

        if self.savings < 0:
            raise ValidationError("Savings cannot be less than zero")
        if self.amount <= 0:
            raise ValidationError("Amount cannot be less than or equal to zero")
        if self.expected_contribution <= 0:
            raise ValidationError("Expected Contribution cannot be less than or equal to zero")
