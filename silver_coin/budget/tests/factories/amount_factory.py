from datetime import date
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
    occurred_on = date(2023, 6, 28)
    estimate = None
    period = None