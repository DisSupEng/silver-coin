from factory.django import DjangoModelFactory
from budget.models import Contribution

class ContributionFactory(DjangoModelFactory):
    """
    Factory for the Contribution model.
    """
    class Meta:
        model = Contribution

    amount = 50.25
    # Attributes set during the test
    goal = None
    budget_period = None
    occurred_on = None 