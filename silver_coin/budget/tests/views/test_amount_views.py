from django.contrib.auth.models import User
from django.urls import reverse

from ..helpers import Authenticate

from ..factories import BudgetFactory
from ..factories import AmountFactory


class AmountViewTests(Authenticate):
    """
    Test cases for the amount views
    """

    def setUp(self):
        """
        Creates the budget to attach the amounts to and logs the user in.
        """
        super().setUp()
        self.budget = BudgetFactory.create(owner=self.user)

        self.second_user = User.objects.create(username="testUser2")
        self.second_user.set_password("test123")
        self.second_user.save()

    def test_income_create_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'create_income` if they are not authorised.
        """
        response = self.client.get(reverse("create_income"))

        self.assertEquals(response.status_code, 302)

    def test_income_create_get(self):
        """
        Tests that the user can get the create income page when logged in
        """
        self.client.login(username="testUser", password="test123")
        response = self.client.get(reverse("create_income"))

        self.assertEquals(200, response.status_code)
        self.assertContains(response, "Create Income")

    def test_income_create_post(self):
        """
        Tests that the user can post and create an income.
        """
        pass

    def test_income_edit_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'edit_income` if they are not authorised.
        """
        # Create a test amount
        test_amount = AmountFactory.create(
            name="Work",
            budget=self.budget,
            amount_type="IN"
        )

        response = self.client.get(reverse("edit_income", kwargs={"pk": test_amount.amount_id}))
        self.assertEquals(response.status_code, 302)


    def test_income_edit_redirect_not_owner(self):
        """
        Tests that the user is redirected to the dashboard if they try to edit an income that is not theirs.
        """
        self.client.login(username="testUser2", password="test1234")

        test_amount = AmountFactory.create(
            name="Work",
            budget=self.budget,
            amount_type="IN"
        )

        response = self.client.get(reverse("edit_income", kwargs={"pk": test_amount.amount_id}))
        self.assertEquals(response.status_code, 302)

    def test_income_edit_get(self):
        """
        Tests that the user can access incomes that they own
        """
        self.client.login(username="testUser", password="test123")

        test_amount = AmountFactory.create(
            name="Work",
            budget=self.budget,
            amount_type="IN"
        )

        response = self.client.get(reverse("edit_income", kwargs={"pk": test_amount.amount_id}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Edit Income")

    def test_income_edit_post(self):
        """
        Tests that the user can post to edit an income
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
