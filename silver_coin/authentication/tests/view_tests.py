from django.test import TestCase
from django.test.client import Client

class IndexTests(TestCase):
    """
    The tests for the Welcome page of the website.
    """
    def test_response_not_authenticated(self):
        """
        A user should be able to view the welcome page when logged out.
        """
        pass

    def test_response_authenticated(self):
        """
        A user should be redirected to the dashboard when authenticated.
        """
        pass

    def test_actions(self):
        """
        There should be two buttons, Sign Up and Login.
        """
        pass

class SignUpTests():
    """
    The tests for the Sign Up page
    """
    def test_response(self):
        """
        Any user should be able to view the Sign Up page.
        """
