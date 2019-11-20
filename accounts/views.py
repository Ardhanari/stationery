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
    """
    Displays form used to log in 
    and authenticates a user
    """

    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST["username"], password=request.POST["password"])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "Login succesful")
            else:
                login_form.add_error(None, "Incorrect username or password")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})

def signup(request):
    """Returns sign up form"""

    return render(request, 'signup.html')
