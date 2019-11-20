from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages

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

    # messages.success(request, "Login succesful")
    return render(request, 'login.html')

def register(request):
    """Returns sign up form"""

    return render(request, 'signup.html')
    