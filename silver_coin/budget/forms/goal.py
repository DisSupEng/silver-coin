from django import forms

from budget.models import Goal

class GoalForm(forms.ModelForm):
    """
    The form that will be used for creating and editing Goals.

    Note that the owner and budget will be set in the view.
    """
    class Meta:
        model = Goal
        fields = ["name", "amount", "expected_contribution"]
    