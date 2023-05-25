from django import forms

from ..models import Amount

class AmountForm(forms.ModelForm):
    """
    The form class for the Amount model.
    Only two fields are needed the name and amount.
    The other fields such as budget, owner, is_one_time_cost, is_actual will be filled in my the view automatically.
    """
    class Meta:
        model = Amount
        fields = ("name", "amount")