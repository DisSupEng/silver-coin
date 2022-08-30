from datetime import datetime, date
from django.core.exceptions import ValidationError

from ..helpers import Authenticate
from ..factories import AmountFactory, BudgetPeriodFactory, BudgetFactory
from ...models import Amount

class BudgetPeriodTests(Authenticate):
    def setUp(self):
        super().setUp()

        self.budget = BudgetFactory.create(owner=self.user)

        AmountFactory.create(
            name="Income",
            amount_type="IN",
            amount=300,
            budget=self.budget,
            owner=self.user
        )
        AmountFactory.create(
            name="Food",
            amount_type="EX",
            amount=100,
            budget=self.budget,
            owner=self.user
        )
        AmountFactory.create(
            name="Power",
            amount_type="EX",
            amount=100,
            budget=self.budget,
            owner=self.user
        )

        self.budget_period = BudgetPeriodFactory.create(budget=self.budget)

    def test_start_date(self):
        self.budget_period.start_date = None
        with self.assertRaisesMessage(ValidationError, "This field cannot be null"):
            self.budget_period.full_clean()


    def test_end_date_days(self):
        self.budget.period_type = "days"
        self.budget.period_length = 4
        self.budget.save()


        self.budget_period = BudgetPeriodFactory.create(start_date=datetime.strptime("2022-08-22", "%Y-%m-%d").date(), budget=self.budget)

        self.assertEquals(self.budget_period.end_date, date(2022, 8, 26))

    def test_end_date_weeks(self):
        self.budget.period_type = "weeks"
        self.budget.period_length = 6
        self.budget.save()

        self.budget_period = BudgetPeriodFactory.create(start_date=datetime.strptime("2022-08-22", "%Y-%m-%d").date(), budget=self.budget)

        self.assertEquals(self.budget_period.end_date, date(2022, 10, 3))

    def test_end_date_months(self):
        self.budget.period_type = "months"
        self.budget.period_length = 9
        self.budget.save()

        self.budget_period = BudgetPeriodFactory.create(start_date=datetime.strptime("2022-08-22", "%Y-%m-%d").date(), budget=self.budget)

        self.assertEquals(self.budget_period.end_date, date(2023, 5, 22))

    def test_is_ended(self):
        self.assertEquals(self.budget_period.is_ended(), True)

    def test_amounts(self):
        # Check that the period contains the estimates
        estimates = self.budget_period.amount_set.filter(is_actual=False)
        self.assertEquals(estimates.count(), 3)

        # Check that the is actual amounts are 0
        actuals = self.budget_period.amount_set.filter(is_actual=True)
        self.assertEquals(actuals.count(), 3)
        # All actual amounts should be 0
        for actual in actuals.all():
            self.assertEquals(actual.amount, 0)
    