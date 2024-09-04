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
        )
        AmountFactory.create(
            name="Food",
            amount_type="EX",
            amount=100,
            budget=self.budget,
        )
        AmountFactory.create(
            name="Power",
            amount_type="EX",
            amount=100,
            budget=self.budget,
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


        self.budget_period = BudgetPeriodFactory.create(start_date=date(2022, 8, 22), budget=self.budget)

        self.assertEquals(self.budget_period.end_date, date(2022, 8, 25))

    def test_end_date_weeks(self):
        self.budget.period_type = "weeks"
        self.budget.period_length = 6
        self.budget.save()

        self.budget_period = BudgetPeriodFactory.create(start_date=date(2022, 8, 22), budget=self.budget)

        self.assertEquals(self.budget_period.end_date, date(2022, 10, 2))

    def test_end_date_months(self):
        self.budget.period_type = "months"
        self.budget.period_length = 9
        self.budget.save()


        self.budget_period = BudgetPeriodFactory.create(start_date=date(2022, 8, 22), budget=self.budget)

        self.assertEquals(self.budget_period.end_date, date(2023, 5, 21))

    def test_is_ended(self):
        self.assertEquals(self.budget_period.is_ended(), True)

    def test_amounts(self):
        # Check that the period contains the estimates
        estimates = self.budget_period.estimates.all()
        self.assertEquals(estimates.count(), 3)

    def test_date_overlap_start_date(self):
        self.budget.period_type = "days"
        self.budget.period_length = 7
        self.budget.save()

        self.budget_period.start_date = date(2023, 7, 1)
        self.budget_period.end_date = date(2023, 7, 8)
        self.budget_period.save()

        self.assertEquals(self.budget_period.start_date, date(2023, 7, 1))
        self.assertEquals(self.budget_period.end_date, date(2023, 7, 7))

        overlapping_period = BudgetPeriodFactory.build(start_date=date(2023, 7, 2), budget=self.budget)

        with self.assertRaisesMessage(ValidationError, "Budget Period overlaps with existing period, please check the dates and try again!"):
            overlapping_period.full_clean()
        
    def test_date_overlap_end_date(self):
        self.budget.period_type = "days"
        self.budget.period_length = 7
        self.budget.save()

        self.budget_period.start_date = date(2023, 7, 1)
        self.budget_period.end_date = date(2023, 7, 8)
        self.budget_period.save()

        self.assertEquals(self.budget_period.start_date, date(2023, 7, 1))
        self.assertEquals(self.budget_period.end_date, date(2023, 7, 7))

        overlapping_period = BudgetPeriodFactory.build(
            start_date=date(2023, 6, 30), 
            budget=self.budget
        )

        with self.assertRaisesMessage(ValidationError, "Budget Period overlaps with existing period, please check the dates and try again!"):
            overlapping_period.full_clean()
    