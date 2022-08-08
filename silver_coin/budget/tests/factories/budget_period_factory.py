from factory import SubFactory
from factory.django import DjangoModelFactory

from ...models import BudgetPeriod, Budget

class BudgetPeriodFactory(DjangoModelFactory):
    class Meta:
        model = BudgetPeriod

    start_date = "2022-08-09"
    # TODO: Implement Budget Factory
    budget = None