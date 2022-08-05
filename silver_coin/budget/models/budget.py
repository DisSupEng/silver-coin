from django.db import models
from django.contrib.auth.models import User

from ..helpers import DAYS, WEEKS, MONTHS, YEARS

class Budget(models.Model):
    """
    This model is the core of the project and what the other models will be based around.
    """

    PERIOD_CHOICES = [
        (DAYS, "Days"),
        (WEEKS, "Weeks"),
        (MONTHS, "Months"),
        (YEARS, "Years"),
    ]

    budget_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, null=False, blank=False, verbose_name="Name")
    description = models.TextField(max_length=250, null=False, blank=True, default="", verbose_name="Description")
    # est_expenses are defined on the Amount model
    # est_incomes are defined on the Amount model
    period_type = models.CharField(choices=PERIOD_CHOICES, null=False, blank=False, max_length=6, default="weeks", verbose_name="Period Type")
    period_length = models.IntegerField(null=False, blank=False, default=1, verbose_name="Period Length")
    # Link to the User so that we can easily filter by the logged in User
    owner = models.ForeignKey(User, null=False, blank=True, editable=False, on_delete=models.CASCADE, db_column="owner")