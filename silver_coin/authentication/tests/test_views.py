from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

class ClientSetup(TestCase):
    def setUp(self):
        self.client = Client()

class IndexTests(ClientSetup):
    """
    The tests for the Welcome page of the website.
    """
    def test_response_not_authenticated(self):
        """
        A user should be able to view the welcome page when logged out.
        """
        response = self.client.get(reverse("index"))
        
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Sign Up")

class SignUpTests(ClientSetup):
    """
    The tests for the Sign Up page
    """
    def test_response(self):
        """
        Any user should be able to view the Sign Up page.
        """
        response = self.client.get(reverse("signup"))

        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Username")
        self.assertContains(response, "Email"),
        self.assertContains(response, "Password")
        self.assertContains(response, "Password Confirmation")

    def test_signup_post(self):
        """
        A user should be able to sign up through a valid post request.
        """
        signup_data = {
            "username": "testUser",
            "email": "test@example.com",
            "password": "test12345",
            "password_confirmation": "test12345"
        }
        response = self.client.post(reverse("signup"), data=signup_data)

        self.assertEquals(response.status_code, 302)

class LoginTests(ClientSetup):
    """
    The tests for the login page
    """
    def test_response(self):
        """
        A user should be able to view the login page.
        """
        response = self.client.get(reverse("login"))

        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Username")
        self.assertContains(response, "Password")

    def test_login_post(self):
        """
        A user should be able to login through a valid post.
        """
        test_user = User.objects.create(username="testUser")
        test_user.set_password("test12345")
        test_user.save()

        login_data = {
            "username": "testUser",
            "password": "test12345"
        }

        response = self.client.post(reverse("login"), data=login_data)

        self.assertEquals(response.status_code, 302)