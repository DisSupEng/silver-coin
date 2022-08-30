from django.core.exceptions import ValidationError

from ..helpers import Authenticate
from ..factories import AmountFactory, BudgetFactory, BudgetPeriodFactory


class AmountTests(Authenticate):
    """
    The tests for the amount model.
    """

    def setUp(self):
        """
        Creates a Amount object for testing
        """
        super().setUp()
        budget = BudgetFactory.create(owner=self.user)
        
        self.amount = AmountFactory.create(budget=budget, owner=self.user)


    def test_name_blank(self):
        self.amount.name = None
        with self.assertRaisesMessage(ValidationError, "This field cannot be null"):
            self.amount.full_clean()

        self.amount.name = ""
        with self.assertRaisesMessage(ValidationError, "This field cannot be blank"):
            self.amount.full_clean()

    def test_amount_type_invalid(self):
        self.amount.amount_type = "IV"
        with self.assertRaisesMessage(ValidationError, "Value \'IV\' is not a valid choice"):
            self.amount.full_clean()

    def test_amount_greater_than_zero(self):
        self.amount.amount = -1
        with self.assertRaisesMessage(ValidationError, "Amount must be greater than zero, mark as expense if outgoing cost"):
            self.amount.full_clean()

        self.amount.amount = 0
        with self.assertRaisesMessage(ValidationError, "Amount must be greater than zero, mark as expense if outgoing cost"):
            self.amount.full_clean()

    def test_amount_no_link_to_budget_or_period(self):
        self.amount.budget = None
        with self.assertRaisesMessage(ValidationError, "An Amount must be linked to either a Budget or BudgetPeriod"):
            self.amount.full_clean()

    def test_amount_link_to_both_budget_and_period(self):
        budget_period = BudgetPeriodFactory.create(budget=self.amount.budget)
        self.amount.budget_period = budget_period
        with self.assertRaisesMessage(ValidationError, "An Amount cannot be linked to both a Budget and BudgetPeriod"):
            self.amount.full_clean()

    def test_no_owner(self):
        self.amount.owner = None
        with self.assertRaisesMessage(ValidationError, "Amount must be linked to a User"):
            self.amount.full_clean()
