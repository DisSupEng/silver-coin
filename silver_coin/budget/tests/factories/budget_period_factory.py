from datetime import datetime
from factory.django import DjangoModelFactory

from ...models import BudgetPeriod

class BudgetPeriodFactory(DjangoModelFactory):
    class Meta:
        model = BudgetPeriod

    start_date = datetime.strptime("2022-08-09", "%Y-%M-%d").date()
    # The Budget is assigned in the tests
    budget = None