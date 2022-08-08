from factory import SubFactory
from factory.django import DjangoModelFactory
from ...models import Amount

class AmountFactory(DjangoModelFactory):
    class Meta:
        model = Amount

    name = "Food"
    amount_type = "EX"
    # TODO: Implement budget factory
    budget = None
    budget_period = None
    # TODO: Implement User factory
    owner = None