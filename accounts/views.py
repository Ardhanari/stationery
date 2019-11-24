from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from checkout.models import Order, OrderLineItem
from accounts.forms import UserLoginForm, SignUpNewUserForm
from products.forms import ProductReviewForm

def index(request):
    """Return index.html file"""

    return render(request, 'index.html')

@login_required
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
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST["username"], password=request.POST["password"])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "Login succesful")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Incorrect username or password")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})

def signup(request):
    """Returns sign up form"""
    if request.user.is_authenticated:
        return redirect(reverse('index')) 

    if request.method == 'POST':
        signup_form = SignUpNewUserForm(request.POST)

        if signup_form.is_valid():
            signup_form.save()

            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "Account created")
            else:
                messages.error(request, "Couldn't create your account this time, try again later")
    else:
        signup_form = SignUpNewUserForm()

    return render(request, 'signup.html', {'signup_form': signup_form})

def user_profile(request):
    """
    Renders user profile page. Displays user data based on email stored in db
    """
    user = User.objects.get(email=request.user.email)
    
    try: 
        orders = Order.objects.get(user=request.user.username)
        return render(request, 'userprofile.html', {"profile": user, 'orders': orders})
    except: 
        return render(request, 'userprofile.html', {"profile": user})

def view_order(request, id):
    """
    Renders overview of an order placed by the user 
    Allows to write the review 
    """
    user = User.objects.get(email=request.user.email)
    selectedorder = Order.objects.get(id=id)
    review_form = ProductReviewForm()

    return render(request, 'vieworder.html', {'selected_order': selectedorder, 'review_form': review_form })



