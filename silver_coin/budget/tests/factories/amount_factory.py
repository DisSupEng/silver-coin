from factory import SubFactory
from factory.django import DjangoModelFactory
from ...models import Amount

class AmountFactory(DjangoModelFactory):
    class Meta:
        model = Amount

    name = "Food"
    amount_type = "EX"
    amount = 100
    # These fields are set in the tests
    budget = None
    budget_period = None