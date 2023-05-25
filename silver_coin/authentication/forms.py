from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")
        help_texts = {"username": ""}

    # Password fields are not model related
    password = forms.CharField(required=True, min_length=8, widget=forms.PasswordInput, label="Password")
    password_confirmation = forms.CharField(required=True, min_length=8, widget=forms.PasswordInput, label="Password Confirmation")


    def clean(self):
        """
        A custom clean method that checks the password and password confirmation fields match.
        Calls the parent clean method after confirming the passwords match.
        """
        password_clean = self.cleaned_data["password"]
        password_confirmation_clean = self.cleaned_data["password_confirmation"]

        # Check that the passwords match
        if password_clean != password_confirmation_clean:
            raise ValidationError("Password fields do not match. Please check your given password and try again")

        return super().clean()