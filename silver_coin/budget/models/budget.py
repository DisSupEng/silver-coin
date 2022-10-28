from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.core.exceptions import ValidationError

from ..helpers import PERIOD_CHOICES

class Budget(models.Model):
    """
    This model is the core of the project and what the other models will be based around.
    """
    budget_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, validators=[MaxLengthValidator(25, "Name cannot be greater than 25 characters")], null=False, blank=False, verbose_name="Name")
    description = models.TextField(max_length=250, validators=[MaxLengthValidator(250, "Description cannot be greater than 250 characters")], null=False, blank=True, default="", verbose_name="Description")
    # est_expenses are defined on the Amount model
    # est_incomes are defined on the Amount model
    period_type = models.CharField(choices=PERIOD_CHOICES, null=False, blank=False, max_length=6, default="weeks", verbose_name="Period Type")
    period_length = models.IntegerField(validators=[MinValueValidator(1, "Period Length must be greater than zero")], null=False, blank=False, default=1, verbose_name="Period Length")
    # Link to the User so that we can easily filter by the logged in User
    owner = models.ForeignKey(User, null=False, editable=False, on_delete=models.CASCADE, db_column="owner")

    def clean(self):
        """
        Add a custom validator that checks whether the Budget has a user.
        It is easier to catch it here than waiting for it to hit the database/
        """
        try:
            self.owner
        except User.DoesNotExist:
            raise ValidationError("Budget must be linked to a User")