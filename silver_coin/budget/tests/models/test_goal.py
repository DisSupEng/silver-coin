from datetime import date
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from budget.tests.helpers import Authenticate
from budget.tests.factories import BudgetFactory, BudgetPeriodFactory, ContributionFactory, GoalFactory

class GoalTests(Authenticate):
    """
    Tests for the Goal model.
    """
    def setUp(self):
        """
        Sets up the data for the tests.
        """
        super().setUp()
        self.budget = BudgetFactory(owner=self.user)

    def test_budget_validation(self):
        """
        A goal should not be valid if a budget is not attached.
        """
        with self.assertRaises(IntegrityError, msg="Goal is not valid when budget is not attached"):
            GoalFactory()
    
    def test_amount_validation(self):
        """
        Tests that a goal is valid when the amount is greater than zero.
        """

        goal = GoalFactory(budget=self.budget)
        try:
            goal.full_clean()
        except ValidationError:
            self.fail("Goal should be valid with an amount greater than zero")

        goal.amount = -100

        with self.assertRaisesMessage(ValidationError, "Amount must be greater than zero"):
            goal.full_clean()

        goal.amount = 0

        with self.assertRaisesMessage(ValidationError, "Amount must be greater than zero"):
            goal.full_clean()

    def test_expected_contribution_validation(self):
        """
        Tests that a goal is valid when the expected_contribution is greater than zero.
        """

        goal = GoalFactory(budget=self.budget)
        try:
            goal.full_clean()
        except ValidationError:
            self.fail("Goal should be valid with an expected contribution greater than zero")

        goal.expected_contribution = -100

        with self.assertRaisesMessage(ValidationError, "Expected contribution must be greater than zero"):
            goal.full_clean()

        goal.expected_contribution = 0

        with self.assertRaisesMessage(ValidationError, "Expected contribution must be greater than zero"):
            goal.full_clean()

    def test_valid_goal(self):
        """
        Test that a Goal with valid data can be saved.
        """
        goal = GoalFactory(budget=self.budget)
        goal.full_clean()
        goal.save()

class ContributionTests(Authenticate):
    """
    Tests for the Contribution model.
    """
    def setUp(self):
        """
        Creates a BudgetPeriod and Goal for the test cases.
        """
        super().setUp()

        self.budget = BudgetFactory(owner=self.user)
        self.budget_period = BudgetPeriodFactory(budget=self.budget, start_date=date(2025, 10, 24))
        self.goal = GoalFactory(budget=self.budget)

    def test_invalid_occurred_on(self):
        """
        Tests that a Contribution is invalid if it occurs outside the BudgetPeriod date range.
        """
        contribution = ContributionFactory(
            goal=self.goal,
            budget_period=self.budget_period,
            occurred_on=date(1999, 1, 1)
        )

        with self.assertRaisesMessage(ValidationError, "Occurred On must be greater than or equal to period start date"):
            contribution.full_clean()

        contribution.occurred_on = date(2050, 1, 1)

        with self.assertRaisesMessage(ValidationError, "Occurred On must be less than or equal to the end date"):
            contribution.full_clean()

        contribution.occurred_on = date(2025, 10, 25)
        # A validation error should not be raised
        contribution.full_clean()

    def test_invalid_goal(self):
        """
        Tests that a Contribution is invalid if not linked to a Goal.
        """
        with self.assertRaises(IntegrityError, msg="Contribution is invalid without a Goal"):
            contribution = ContributionFactory(
                goal=None,
                budget_period=self.budget_period,
                occurred_on=date(2025, 10, 25)
            )

    def test_invalid_budget_period(self):
        """
        Tests that a Contribution is invalid if not linked to a BudgetPeriod.
        """
        with self.assertRaises(IntegrityError, msg="Contribution is invalid without a BudgetPeriod"):
            contribution = ContributionFactory(
                goal=self.goal,
                budget_period=None,
                occurred_on=date(2025, 10, 25)
            )

    def test_invalid_amount(self):
        """
        Tests that a Contribution is invalid when the amount is less than 0.1.
        """
        contribution = ContributionFactory(
            goal=self.goal,
            budget_period=self.budget_period,
            occurred_on=date(2025, 10, 25),
            amount=-100
        )

        with self.assertRaisesMessage(ValidationError, "Amount must be greater than or equal to 0.1"):
            contribution.full_clean()

        contribution.amount = 0.01

        with self.assertRaisesMessage(ValidationError, "Amount must be greater than or equal to 0.1"):
            contribution.full_clean()

        contribution.amount = 100
        contribution.full_clean()
