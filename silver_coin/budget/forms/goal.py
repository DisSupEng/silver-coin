from django import forms

from budget.models import Contribution, Goal

class GoalForm(forms.ModelForm):
    """
    The form that will be used for creating and editing Goals.

    Note that the owner and budget will be set in the view.
    """
    class Meta:
        model = Goal
        fields = ["name", "amount", "expected_contribution"]

class ContributionForm(forms.ModelForm):
    """
    The form that will be used for creating and editing Contributions.
    """
    class Meta:
        model = Contribution
        fields = ["amount", "occurred_on", "goal"]
    