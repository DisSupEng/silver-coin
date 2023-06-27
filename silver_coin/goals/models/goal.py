from django.contrib.auth.models import User
from django.db import models

class Goal(models.Model):
    """
    A goal represents something that the user wants to save for.
    """
    name = models.CharField(max_length=255, null=False, blank=False)
    amount = models.DecimalField(null=False, blank=False, max_digits=7, decimal_places=2)

    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="goals")