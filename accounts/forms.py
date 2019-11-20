from django import forms

class UserLoginForm(forms.Form):
    """Log in form"""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)