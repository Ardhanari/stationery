from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from checkout.models import Order, OrderLineItem
from accounts.forms import UserLoginForm, SignUpNewUserForm, ShippingAddressForm
from accounts.models import ShippingAddress
from products.forms import ProductReviewForm
from products.models import Product, ProductReview

def index(request):
    """Returns index.html file"""
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
    Renders user profile page. 
    Tries for data on user orders - if that information is available renders page with orders and shipping address,
    otherwise it's just user profile without any additional context. 
    """
    user = request.user
    
    try: 
        orders = Order.objects.all().filter(user=user).order_by('-date')
        shipping_address = ShippingAddress.objects.get(user=user)
        return render(request, 'userprofile.html', {"profile": user, 'orders': orders, 'shipping_address': shipping_address})
        # try:
        #     shipping_address = ShippingAddress.objects.get(user=user)
        #     return render(request, 'userprofile.html', {"profile": user, 'orders': orders, 'shipping_address': shipping_address})
        # except:
        #     return render(request, 'userprofile.html', {"profile": user, 'orders': orders})     
    except: 
        return render(request, 'userprofile.html', {"profile": user})

def view_order(request, id):
    """
    Renders overview of an order placed by the user 
    Allows to write the review of product bought
    """
    user = request.user
    selected_order = Order.objects.get(id=id)
    order_items = list(OrderLineItem.objects.all().filter(order=selected_order))
    review_form = ProductReviewForm()

    user_reviews = list(ProductReview.objects.all().filter(author=user))

    if user_reviews:
        return render(request, 'vieworder.html', {'selected_order': selected_order, 'order_items': order_items, 'review_form': review_form, 'user_reviews': user_reviews })
    else:            
        return render(request, 'vieworder.html', {'selected_order': selected_order, 'order_items': order_items, 'review_form': review_form })

def submit_product_review(request, id):
    """
    Allows user to add or update a review to product they bought
    User can only review product once, even if got it multiple times in different orders 
    User can update the review how many times they wish
    """
    previous_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':

        review_form = ProductReviewForm(request.POST)
        user = request.user

        if review_form.is_valid():
            try:
                review = ProductReview.objects.get(author_id=user, product_id=id)
                review_form = review_form.save(commit=False)
                review_form.author = user
                review_form.product_id = id
                review_form.id = review.id # makes sure to overwrite existing row instead of creating new one
                review_form.save()
                messages.success(request, "Your review was updated")
            except:
                review_form = review_form.save(commit=False)
                review_form.author = user
                review_form.product_id = id
                review_form.save()
                messages.success(request, "Your review was saved")

        else:
            messages.error(request, "Something went wrong!")
    
    return redirect(previous_url)

def edit_your_address(request):
    """
    Allows user to edit their address stored in db. 
    Currently only one address per user is allowed
    """

    user = request.user
    address_exists = ShippingAddress.objects.get(user=user)
    shipping_address = ShippingAddress.objects.get(user=user)

    # prepopulates form with existing data
    shipping_address_form = ShippingAddressForm(initial={'full_name': address_exists.full_name, 'company': address_exists.company, 
                                                                'street_address1': address_exists.street_address1, 'street_address2': address_exists.street_address2,
                                                                'postcode': address_exists.postcode, 'town_or_city': address_exists.town_or_city, 
                                                                'county': address_exists.country, 'country': address_exists.country, 
                                                                'phone_number': address_exists.phone_number
                                                                }, auto_id=False)

    if request.method == "POST":
        shipping_address_form = ShippingAddressForm(request.POST) 

        if shipping_address_form.is_valid():
            shipping_address = shipping_address_form.save(commit=False)
            shipping_address.user = user
            shipping_address.id = ShippingAddress.objects.get(user=user).id
            shipping_address.save()
            messages.success(request, "Address saved")
            return redirect(reverse('userprofile'))     
        else:
            messages.warning(request, "Your changes weren't saved. Make sure all fields are filled correctly.")                                                               
            return redirect(reverse('edityouraddress'))     

    return render(request, "editaddress.html", {'shipping_form': shipping_address_form})        

def delete_your_address(request):
    """
    Deletes user's shipping address from the database
    Will be reinstated after changing Order and ShippingAddres structure and relation
    that will allow to delete address (ShippingAddress) but keep the address in Order model
    """
    pass