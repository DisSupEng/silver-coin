from django import forms

from ..models import Amount

class AmountForm(forms.Form):
    """
    The form class for the Amount model.
    Only two fields are needed the name and amount.
    The other fields such as budget, owner, is_one_time_cost, is_actual will be filled in my the view automatically.
    """
    class Meta:
        model = Amount
        fields = ("name", "amount")

    name = forms.CharField(required=True, max_length=50)
    amount = forms.DecimalField(max_digits=7, decimal_places=2)

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Amount
        fields = ("name", "amount")