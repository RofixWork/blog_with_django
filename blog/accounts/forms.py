from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User


class RegsiterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        help_text="Enter the same password as before, for verification.",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
