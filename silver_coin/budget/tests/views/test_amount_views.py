from ..helpers import Authenticate

from ...models import Amount
from ...models import Budget

class AmountViewTests(Authenticate):
    """
    Test cases for the amount views
    """

    def setUp(self):
        """
        Creates the budget to attach the amounts to and logs the user in.
        """
        pass

    def test_income_create_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'create_income` if they are not authorised.
        """
        pass

    def test_income_edit_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'edit_income` if they are not authorised.
        """
        pass

    def test_income_edit_redirect_not_owner(self):
        """
        Tests that the user is redirected to the dashboard if they try to edit an income that is not theirs.
        """
        pass

    def test_income_delete_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'delete_income` if they are not authorised.
        """
        pass

    def test_income_delete_redirect_not_owner(self):
        """
        Tests that the user is redirected to the dashboard if they try to delete an income that is not theirs.
        """
        pass

    def test_expense_create_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'create_expense` if they are not authorised.
        """
        pass

    def test_expense_edit_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'edit_expense` if they are not authorised.
        """
        pass

    def test_expense_edit_redirect_not_owner(self):
        """
        Tests that the user is redirected to the dashboard if they try to edit an expense that is not theirs.
        """
        pass

    def test_expense_delete_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'delete_expense` if they are not authorised.
        """
        pass

    def test_expense_delete_redirect_not_owner(self):
        """
        Tests that the user is redirected to the dashboard if they try to delete an expense that is not theirs.
        """
        pass
