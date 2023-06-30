from datetime import datetime
from django.core.exceptions import ValidationError

from ..helpers import Authenticate
from ..factories import ActualAmountFactory
from ..factories import AmountFactory
from ..factories import BudgetFactory
from ..factories import BudgetPeriodFactory


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
        
        self.amount = AmountFactory.create(budget=budget)


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

class ActualAmountTests(Authenticate):
    """
    Tests for the ActualAmount model.
    """
    def setUp(self):
        """
        Creates a ActualAmount object for testing
        """
        super().setUp()
        budget = BudgetFactory.create(owner=self.user)
        amount = AmountFactory.create(budget=budget)

        self.period = BudgetPeriodFactory.create(
            start_date=datetime.strptime("2023-06-28", "%Y-%M-%d").date(),
            budget=budget
        )

        self.actual_amount = ActualAmountFactory.create(
            estimate=amount,
            period=self.period
        )

    def test_name_blank(self):
        self.actual_amount.name = None
        with self.assertRaisesMessage(ValidationError, "This field cannot be null"):
            self.actual_amount.full_clean()

        self.actual_amount.name = ""
        with self.assertRaisesMessage(ValidationError, "This field cannot be blank"):
            self.actual_amount.full_clean()

    def test_amount_blank(self):
        self.actual_amount.amount = None
        with self.assertRaisesMessage(ValidationError, "This field cannot be null"):
            self.actual_amount.full_clean()

    def test_amount_greater_than_zero(self):
        self.actual_amount.amount = -1
        with self.assertRaisesMessage(ValidationError, "Amount must be greater than zero"):
            self.actual_amount.full_clean()

        self.actual_amount.amount = 0
        with self.assertRaisesMessage(ValidationError, "Amount must be greater than zero"):
            self.actual_amount.full_clean()

    def test_occurred_on_blank(self):
        self.actual_amount.occurred_on = None
        with self.assertRaisesMessage(ValidationError, "This field cannot be null"):
            self.actual_amount.full_clean()

    def test_occurred_on_greater_than_period_start(self):
        self.actual_amount.occurred_on = datetime.strptime("2023-05-28", "%Y-%M-%d").date()
        with self.assertRaisesMessage(ValidationError, "Occurred On must be greater than or equal to period start date"):
            self.actual_amount.full_clean()
    
    def test_occurred_on_less_than_period_end(self):
        self.actual_amount.occurred_on = datetime.strptime("2023-06-05", "%Y-%M-%d").date()
        with self.assertRaisesMessage(ValidationError, "Occurred On must be less than end date"):
            self.actual_amount.full_clean()
