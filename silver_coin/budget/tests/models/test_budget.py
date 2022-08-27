from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..factories import BudgetFactory

class Authenticate(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testUser")
        self.user.set_password("test123")
        self.user.save()

class BudgetTests(Authenticate):

    def setUp(self):
        """
        This method creates a budget model under the class for use in the tests.
        """
        # Create a user to link the budget to
        super().setUp()
        # Create a budget to run tests on
        self.budget = BudgetFactory.create(owner=self.user)


    def test_name_character_limit(self):
        self.budget.name = "t" * 26
        with self.assertRaisesMessage(ValidationError, "Name cannot be greater than 25 characters"):
            self.budget.full_clean()

    def test_description_character_limit(self):
        self.budget.description = "t" * 251
        with self.assertRaisesMessage(ValidationError, "Description cannot be greater than 250 characters"):
            self.budget.full_clean()

    def test_invalid_period_type(self):
        self.budget.period_type = "invalid"
        with self.assertRaisesMessage(ValidationError, "Value \'invalid\' is not a valid choice."):
            self.budget.full_clean()

    def test_invalid_period_length(self):
        self.budget.period_length = 0
        with self.assertRaisesMessage(ValidationError, "Period Length must be greater than zero"):
            self.budget.full_clean()

        self.budget.period_length = -50
        with self.assertRaisesMessage(ValidationError, "Period Length must be greater than zero"):
            self.budget.full_clean()

    def test_no_owner(self):
        self.budget.owner = None
        with self.assertRaisesMessage(ValidationError, "Budget must be linked to a User"):
            self.budget.full_clean()

    # TODO: Add tests for expenses and incomes
    def test_get_expenses(self):
        pass

    def test_get_incomes(self):
        pass