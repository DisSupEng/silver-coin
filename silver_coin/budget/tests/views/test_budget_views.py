from django.test import Client
from django.urls import reverse

from ..helpers import Authenticate

class BudgetCreateView(Authenticate):
    """
    Tests the budget creation views
    """
    def setUp(self):
        super().setUp()

        self.client = Client()
        self.client.login(username="testUser", password="test123")

    def test_budget_create_get(self):
        response = self.client.get(reverse("create_budget"))

        self.assertEquals(response.status_code, 200)
        # Core budget attributes
        self.assertContains(response, "name=\"name\"")
        self.assertContains(response, "name=\"description\"")
        self.assertContains(response, "name=\"period_type\"")
        self.assertContains(response, "name=\"period_length\"")

    def test_budget_create_post(self):
        pass


