from datetime import date
from factory.django import DjangoModelFactory

from ...models import BudgetPeriod

class BudgetPeriodFactory(DjangoModelFactory):
    class Meta:
        model = BudgetPeriod

    start_date = date(2022, 8, 9)
    # The Budget is assigned in the tests
    budget = None