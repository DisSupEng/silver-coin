from factory import SubFactory
from factory.django import DjangoModelFactory
from ...models import Amount

class AmountFactory(DjangoModelFactory):
    class Meta:
        model = Amount

    name = "Food"
    amount_type = "EX"
    amount = 100
    is_actual = False
    is_one_time_cost = False
    # These fields are set in the tests
    budget = None
    budget_period = None
    owner = None