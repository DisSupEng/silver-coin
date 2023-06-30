from datetime import datetime
from factory.django import DjangoModelFactory
from ...models import Amount
from ...models import ActualAmount

class AmountFactory(DjangoModelFactory):
    """
    Factory for the Amount model.
    """
    class Meta:
        model = Amount

    name = "Food"
    amount_type = "EX"
    amount = 100
    # These fields are set in the tests
    budget = None
    budget_period = None

class ActualAmountFactory(DjangoModelFactory):
    """
    Factory for the ActualAmount model.
    """
    class Meta:
        model = ActualAmount
    
    name = "Countdown"
    amount = "25.76"
    occurred_on = datetime.strptime("2023-06-28", "%Y-%M-%d").date()
    estimate = None
    period = None