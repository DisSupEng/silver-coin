from factory.django import DjangoModelFactory
from ...models import Budget

class BudgetFactory(DjangoModelFactory):
    class Meta:
        model = Budget
    
    name = "Mock Budget"
    description = "This is a mock budget for testing"
    period_type = "months"
    period_length = 1
    # TODO: Implement owner factory
    owner = None