from ..helpers import Authenticate

class DashboardTests(Authenticate):
    """
    Tests for the dashboard functionality.
    """
    def setUp(self):
        """
        Logs the user in for accessing the dashboard/
        """
        super().setUp()

        self.client.login()


    def test_redirect_if_not_logged_in(self):
        # Log the user out for this test
        self.client.logout()

        response = self.client.get("/dashboard", follow=False)

        self.assertEquals(response.status_code, 302)
        self.assertContains(response, "Login")

    def test_dashboard_cards(self):
        response = self.client.get("/dashboard")

        # Logged in user should be able to view the page
        self.assertEqual(response.status_code, 200)

        # There should be three cards
        self.assertContains(response, "Dashboard")
        self.assertContains(response, "Budget History")
        self.assertContains(response, "Goals")
