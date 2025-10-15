from factory.django import DjangoModelFactory

from budget.models import Goal

class GoalFactory(DjangoModelFactory):
    class Meta:
        model = Goal

    name = "Test Goal"
    amount = 150.75
    expected_contribution = 75.00
    # Budget is assigned in the test
    budget = None
