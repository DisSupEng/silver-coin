from datetime import date
from django import forms

from ..models import BudgetPeriod

class BudgetPeriodForm(forms.Form):
    start_date = forms.DateField(
        required=True, 
        label="Start Date",
        initial=date.today,
        widget=forms.SelectDateWidget(attrs={"class": "browser-default"})
    )

class BudgetPeriodModelForm(forms.ModelForm):
    class Meta:
        model = BudgetPeriod
        fields = ["start_date"]
    
    start_date = forms.DateField(
        required=True, 
        label="Start Date",
        initial=date.today,
        widget=forms.SelectDateWidget(attrs={"class": "browser-default"})
    )