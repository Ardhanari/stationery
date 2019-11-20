from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
    """Log in form"""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpNewUser(forms.Form):
    """Form used to create new instance of user """

    # username = forms.CharField()
    # email = 
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm your password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']