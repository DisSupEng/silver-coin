from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse

from ..helpers import Authenticate

from ..factories import BudgetFactory
from ..factories import AmountFactory

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
        super().setUp()
        self.budget = BudgetFactory.create(owner=self.user)

        self.second_user = User.objects.create(username="testUser2")
        self.second_user.set_password("test123")
        self.second_user.save()

        BudgetFactory.create(owner=self.second_user)

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
        self.client.login(username="testUser", password="test123")

        response = self.client.post(
            reverse("create_income"),
            data={
                "name": "New Income",
                "amount": 78.75
            },
        )
        self.assertEquals(response.status_code, 302)

        test_income = Amount.objects.last()
        self.assertEquals(test_income.name, "New Income")
        self.assertEquals(test_income.amount, 78.75)

    def test_income_create_no_budget(self):
        """
        Tests that the user is redirected to the dashboard on 'create_income' if they do not have a budget.
        """
        self.client.login(username="testUser", password="test123")

        # Remove the user's budget for this test
        Budget.objects.get(owner=self.user).delete()

        response = self.client.get(reverse("create_income"))

        self.assertEquals(response.status_code, 302)

        response = self.client.post(
            reverse("create_income"),
            data={
                "name": "New Income",
                "amount": 78.75
            },
        )
        self.assertEquals(response.status_code, 302)

        # Check that no income was created
        self.assertEquals(Amount.objects.count(), 0)
    


    def test_income_edit_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'edit_income` if they are not authorised.
        """
        # Create a test amount
        test_income = AmountFactory.create(
            name="Work",
            budget=self.budget,
            amount_type="IN"
        )

        response = self.client.get(reverse("edit_income", kwargs={"pk": test_income.amount_id}))
        self.assertEquals(response.status_code, 302)


    def test_income_edit_redirect_not_owner(self):
        """
        Tests that the user recieves a 404 response if they try to access an amount that is not theirs
        """
        self.client.login(username="testUser2", password="test123")

        test_income = AmountFactory.create(
            name="Work",
            budget=self.budget,
            amount_type="IN"
        )

        response = self.client.get(reverse("edit_income", kwargs={"pk": test_income.amount_id}))
        self.assertEquals(response.status_code, 404)

    def test_income_edit_get(self):
        """
        Tests that the user can access incomes that they own
        """
        self.client.login(username="testUser", password="test123")

        test_income = AmountFactory.create(
            name="Work",
            budget=self.budget,
            amount_type="IN"
        )

        response = self.client.get(reverse("edit_income", kwargs={"pk": test_income.amount_id}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Edit Income")

    def test_income_edit_post(self):
        """
        Tests that the user can post to edit an income
        """
        self.client.login(username="testUser", password="test123")

        test_income = AmountFactory.create(
            name="Work",
            budget=self.budget,
            amount_type="IN"
        )

        response = self.client.post(
            reverse("edit_income", kwargs={"pk": test_income.amount_id}),
            data={
                "name":"Work (Updated)",
                "amount": 600,

            }
        )

        updated_income = Amount.objects.get(pk=test_income.amount_id)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(updated_income.name, "Work (Updated)")
        self.assertEquals(updated_income.amount, 600)

    def test_income_delete_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'delete_income` if they are not authorised.
        """
        test_income = AmountFactory.create(
            name="Work",
            budget=self.budget,
            amount_type="IN"
        )

        # Test the get request on the delete_income view
        response = self.client.get(reverse("delete_income", kwargs={"pk": test_income.amount_id}))
        self.assertEquals(response.status_code, 302)

        # Test the get request on the delete_income view
        response = self.client.post(reverse("delete_income", kwargs={"pk": test_income.amount_id}))
        self.assertEquals(response.status_code, 302)


    def test_income_delete_redirect_not_owner(self):
        """
        Tests that the user is redirected to the dashboard if they try to delete an income that is not theirs.
        """
        self.client.login(username="testUser2", password="test123")

        test_income = AmountFactory.create(
            name="Work",
            budget=self.budget,
            amount_type="IN"
        )

        # Test the get request on a delete_income view
        response = self.client.get(reverse("delete_income", kwargs={"pk": test_income.amount_id}))
        self.assertEquals(response.status_code, 404)

        # Test the post request on a delete_income view
        response = self.client.post(reverse("delete_income", kwargs={"pk": test_income.amount_id}))
        self.assertEquals(response.status_code, 404)

    def test_expense_create_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'create_expense` if they are not authorised.
        """
        AmountFactory.create(
            name="Food",
            budget=self.budget,
            amount_type="EX"
        )

        # Test the get request on the create_expense view
        response = self.client.get(reverse("create_expense"))
        self.assertEquals(response.status_code, 302)

        # Test the post request on the create_expense view
        response = self.client.post(
            reverse("create_expense"),
            data={
                "name": "New Expense",
                "amount": 66.50
            }
        )
        self.assertEquals(response.status_code, 302)

    def test_expense_create_redirect_no_budget(self):
        """
        Tests that the user is redirected to the dashboard if they try to create an expense without having a budget.

        If they don't have a budget then they can't have any expenses.
        """
        self.client.login(username="testUser", password="test123")

        # Remove the user's budget for this test
        Budget.objects.get(owner=self.user).delete()

        response = self.client.get(reverse("create_expense"))

        self.assertEquals(response.status_code, 302)

        response = self.client.post(
            reverse("create_expense"),
            data={
                "name": "New Expense",
                "amount": 78.75
            },
        )
        self.assertEquals(response.status_code, 302)

        # Check that no income was created
        self.assertEquals(Amount.objects.count(), 0)

    def test_expense_edit_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'edit_expense` if they are not authorised.
        """
        test_expense = AmountFactory.create(
            name="Food",
            budget=self.budget,
            amount_type="EX"
        )

        # Test the get request on an edit_expense view
        response = self.client.get(reverse("edit_expense", kwargs={"pk": test_expense.amount_id}))
        self.assertEquals(response.status_code, 302)

        # Test the post request on an edit_expense view
        response = self.client.post(
            reverse("edit_expense", kwargs={"pk": test_expense.amount_id}),
            data={
                "name": "Food (Updated)",
                "amount": 75
            }
        )
        self.assertEquals(response.status_code, 302)

    def test_expense_edit_redirect_not_owner(self):
        """
        Tests that the user is redirected to the dashboard if they try to edit an expense that is not theirs.
        """
        self.client.login(username="testUser2", password="test123")

        test_expense = AmountFactory.create(
            name="Food",
            budget=self.budget,
            amount_type="EX"
        )

        # Test the get request on the edit_expense view
        response = self.client.get("edit_expense", kwargs={"pk": test_expense.amount_id})
        self.assertEquals(response.status_code, 404)

        # Test the post request on the edit_expense view
        response = self.client.post(reverse("edit_expense", kwargs={"pk": test_expense.amount_id}))
        self.assertEquals(response.status_code, 404)

    def test_expense_delete_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen on 'delete_expense` if they are not authorised.
        """
        test_expense = AmountFactory.create(
            name="Food",
            budget=self.budget,
            amount_type="EX"
        )

        # Test the get request on the delete_expense view
        response = self.client.get(reverse("delete_expense", kwargs={"pk": test_expense.amount_id}))
        self.assertEquals(response.status_code, 302)

        # Test the post request on the delete_expense view
        response = self.client.post(reverse("delete_expense", kwargs={"pk": test_expense.amount_id}))
        self.assertEquals(response.status_code, 302)

    def test_expense_delete_redirect_not_owner(self):
        """
        Tests that the user is redirected to the dashboard if they try to delete an expense that is not theirs.
        """
        self.client.login(username="testUser2", password="test123")

        test_expense = AmountFactory.create(
            name="Food",
            budget=self.budget,
            amount_type="EX"
        )

        # Test the get request on the delete_expense view
        response = self.client.get(reverse("delete_expense", kwargs={"pk": test_expense.amount_id}))
        self.assertEquals(response.status_code, 404)

        # Test the post request on the delete_expense view
        response = self.client.post(reverse("delete_expense", kwargs={"pk": test_expense.amount_id}))
        self.assertEquals(response.status_code, 404)

class ActualAmountViewTests(Authenticate):
    """
    Tests for the ActualAmount views.
    """
    def setUp(self):
        """
        Creates a budget and amount to test the actual amount views.
        """
        super().setUp()
        self.budget = BudgetFactory.create(owner=self.user)
        self.amount = AmountFactory.create(
            name="Food",
            budget=self.budget,
            amount_type="EX"
        )

        self.second_user = User.objects.create(username="testUser2")
        self.second_user.set_password("test123")
        self.second_user.save()

    def test_create_view_redirect_unauthorised(self):
        """
        Tests that the user is redirected to the login screen if they are unauthorised.
        """
        response = self.client.get(reverse("create_actual_amount"))

        self.assertEquals(response.status_code, 302)

        response = self.client.post(
            reverse("create_actual_amount"),
            data={
                "name": "Countdown",
                "amount": 32.65,
                "occurred_on": datetime.strptime("2023-06-28", "%Y-%M-%d").date(),
                "estimate_id": self.amount.amount_id
            }
        )

        self.assertEquals(response.status_code, 302)

    def test_create_view(self):
        self.client.login(username="testUser", password="test123")

        response = self.client.get(reverse("create_actual_amount"))

        self.assertEquals(response.status_code, 302)

        response = self.client.post(
            reverse("create_actual_amount"),
            data={
                "name": "Countdown",
                "amount": 32.65,
                "occurred_on": datetime.strptime("2023-06-28", "%Y-%M-%d").date(),
                "estimate_id": self.amount.amount_id
            }
        )