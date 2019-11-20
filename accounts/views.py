from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from accounts.forms import UserLoginForm

def index(request):
    """Return index.html file"""

    return render(request, 'index.html')

def logout(request):
    """Logs user out"""

    auth.logout(request)
    messages.success(request, "Logout succesful")
    return redirect(reverse('index'))

def login(request):
    """Logs user in"""

    login_form = UserLoginForm()
    # messages.success(request, "Login succesful")
    return render(request, 'login.html', {'login_form': login_form})

def signup(request):
    """Returns sign up form"""

    return render(request, 'signup.html')
