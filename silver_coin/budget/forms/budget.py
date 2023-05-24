from django import forms
from django.core.validators import MaxLengthValidator, MinValueValidator
from ..helpers import PERIOD_CHOICES
from budget.models import Budget

class BudgetForm(forms.Form):
    name = forms.CharField(max_length=25, validators=[MaxLengthValidator(25, "Name cannot be greater than 25 characters")], required=True, label="Name")
    description = forms.CharField(max_length=250, validators=[MaxLengthValidator(250, "Description cannot be greater than 250 characters")], required=False, label="Description")
    # Need to define the field here so the browser default can be used
    period_type = forms.ChoiceField(
        choices=PERIOD_CHOICES,
        widget=forms.Select(attrs={"class": "browser-default"})
    )
    period_length = forms.IntegerField(validators=[MinValueValidator(1, "Period Length must be greater than zero")], required=True, label="Period Length")

class BudgetModelForm(forms.ModelForm):
    class Meta:
        model = Budget
        exclude = ("owner",)

    period_type = forms.ChoiceField(
        choices=PERIOD_CHOICES,
        widget=forms.Select(attrs={"class": "browser-default"})
    )