from django.core.exceptions import ValidationError

from ..helpers import Authenticate
from ..factories import BudgetFactory, AmountFactory

class BudgetTests(Authenticate):

    def setUp(self):
        """
        This method creates a budget model under the class for use in the tests.
        """
        # Create a user to link the budget to
        super().setUp()
        # Create a budget to run tests on
        self.budget = BudgetFactory.create(owner=self.user)


    def test_name_blank(self):
        self.budget.name = None
        with self.assertRaisesMessage(ValidationError, "This field cannot be null"):
            self.budget.full_clean()
        
        self.budget.name = ""
        with self.assertRaisesMessage(ValidationError, "This field cannot be blank"):
            self.budget.full_clean()
    
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

    def test_get_expenses(self):
        income = AmountFactory.create(
            name="Income",
            amount_type="IN",
            amount=300,
            budget=self.budget
        )
        food_expense = AmountFactory.create(
            name="Food",
            amount_type="EX",
            amount=100,
            budget=self.budget
        )
        power_expense = AmountFactory.create(
            name="Power",
            amount_type="EX",
            amount=100,
            budget=self.budget
        )

        expenses = self.budget.amounts.filter(amount_type="EX")
        self.assertEquals(expenses.count(), 2)

    def test_get_incomes(self):
        income = AmountFactory.create(
            name="Income",
            amount_type="IN",
            amount=300,
            budget=self.budget
        )
        food_expense = AmountFactory.create(
            name="Food",
            amount_type="EX",
            amount=100,
            budget=self.budget
        )
        power_expense = AmountFactory.create(
            name="Power",
            amount_type="EX",
            amount=100,
            budget=self.budget
        )

        income = self.budget.amounts.filter(amount_type="IN")
        self.assertEquals(income.count(), 1)