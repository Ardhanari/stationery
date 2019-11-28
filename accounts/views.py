from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from checkout.models import Order, OrderLineItem
from accounts.forms import UserLoginForm, SignUpNewUserForm
from products.forms import ProductReviewForm
from products.models import Product, ProductReview

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
        orders = list(Order.objects.all().filter(user=request.user.username))
        print("ok")
        return render(request, 'userprofile.html', {"profile": user, 'orders': orders})
    except: 
        return render(request, 'userprofile.html', {"profile": user})

def view_order(request, id):
    """
    Renders overview of an order placed by the user 
    Allows to write the review 
    """
    user = request.user
    selected_order = Order.objects.get(id=id)
    order_items = list(OrderLineItem.objects.all().filter(order=selected_order))
    review_form = ProductReviewForm()

    user_reviews = list(ProductReview.objects.all().filter(author=user))
    # list_of_reviews = list(ProductReview.objects.all().filter(author=user))

    # for review in list_of_reviews:
    #     print(review)
    #     user_reviews.append(review)
    #     print(user_reviews)

    if user_reviews:
        return render(request, 'vieworder.html', {'selected_order': selected_order, 'order_items': order_items, 'review_form': review_form, 'user_reviews': user_reviews })
    else:            
        return render(request, 'vieworder.html', {'selected_order': selected_order, 'order_items': order_items, 'review_form': review_form })

def submit_product_review(request, id):
    """
    Allows user to add a review to product they bought
    """
    previous_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':

        print("POST requested") # sanity check

        review_form = ProductReviewForm(request.POST)

        if review_form.is_valid():
            review_for = Product.objects.get(id=id)

            review_form = review_form.save(commit=False)
            review_form.author = request.user
            review_form.product= review_for
            review_form.save()
            messages.success(request, "Your review was added")
        else:
            messages.error(request, "Something went wrong!")
    
    return redirect(previous_url) #it will redirect back to order view