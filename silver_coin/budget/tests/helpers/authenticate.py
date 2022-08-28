from django.contrib.auth.models import User
from django.test import TestCase

class Authenticate(TestCase):
    """
    This is a helper function that sets up a dummy user for the tests.
    """
    def setUp(self):
        self.user = User.objects.create(username="testUser")
        self.user.set_password("test123")
        self.user.save()