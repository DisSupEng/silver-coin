from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from budget.tests.helpers import Authenticate
from budget.tests.factories import BudgetFactory, GoalFactory

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
