from django.db.models import fields
from chat_app.models import User
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control", "id": "floatingUsername", "placeholder": "Username"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "id": "floatingEmail", "placeholder": "Email"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "floatingPassword1", "placeholder": "Password",
                                          "data-bs-toggle": "tooltip", "data-bs-placement": "bottom", "title":
                                          """Your password can’t be too similar to your other personal information.
                                          Your password must contain at least 8 characters.
                                          Your password can’t be a commonly used password.
                                          Your password can’t be entirely numeric."""}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "floatingPassword2", "placeholder": "Password confirmation"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
