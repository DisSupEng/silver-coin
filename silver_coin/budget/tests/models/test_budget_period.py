from datetime import datetime
from django.core.exceptions import ValidationError

from ..helpers import Authenticate
from ..factories import BudgetPeriodFactory, BudgetFactory

class BudgetPeriodTests(Authenticate):
    def setUp(self):
        super().setUp()

        self.budget = BudgetFactory.create(owner=self.user)
        self.budget_period = BudgetPeriodFactory.create(budget=self.budget)

    def test_start_date(self):
        self.budget_period.start_date = None
        with self.assertRaisesMessage(ValidationError, "This field cannot be null"):
            self.budget_period.full_clean()


    def test_end_date_days(self):
        self.budget.period_type = "days"
        self.budget.period_length = 4
        self.budget.save()


        self.budget_period.start_date = datetime.strptime("2022-08-22", "%Y-%M-%d").date()
        self.budget_period.save()
    