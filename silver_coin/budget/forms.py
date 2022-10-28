from django import forms

from .helpers import PERIOD_CHOICES
from .models import Budget


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ("name", "description", "period_type", "period_length")

    # Need to define the field here so the browser default can be used
    period_type = forms.ChoiceField(
        choices=PERIOD_CHOICES,
        widget=forms.Select(attrs={"class": "browser-default"})
    )

    