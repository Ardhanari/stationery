from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

def view_cart(request):
    """Renders the cart contents page """
    return render(request, "cart.html")

def add_to_cart(request, id):
    """
    Adds product to cart
    Upon completion redirects to the page it was used on 
    """
    previous_url = request.META.get('HTTP_REFERER')
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    
    if id in cart:
        cart[id] = int(cart[id]) + quantity      
    else:
        cart[id] = cart.get(id, quantity) 

    request.session['cart'] = cart

    messages.success(request, "Product added to your cart")
    return redirect(previous_url)

def edit_cart(request, id):
    """
    Allows user to edit quantity of the product in the cart
    if quantity = 0, product is removed from the cart
    """
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[id] = quantity
    else: 
        cart.pop(id)

    request.session['cart'] = cart

    messages.success(request, "Cart updated")
    return redirect(reverse('viewcart'))