from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User
from django.db import models

class Goal(models.Model):
    """
    A Goal is linked to a User and is used to track the money that the user has set
    aside for a particular purpose.

    The model contains the following fields:
    * name: The name of the Goal
    * savings: The current amount that has been saved for this Goal
    * amount: The total cost of this Goal
    * complete: Whether the Goal has been achieved
    * owner: The user that this Goal belongs to
    """
    name = models.CharField(
        max_length=50,
        validators=[MaxLengthValidator(50, "Name cannot be greater than 50 characters")],
        null=False,
        blank=False
    )
    savings = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    complete = models.BooleanField(null=False, blank=False) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
