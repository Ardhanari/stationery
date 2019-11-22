from django.shortcuts import render, redirect, reverse
from django.contrib import messages

def view_cart(request):
    """Renders the cart contents page """
    return render(request, "cart.html")

def add_to_cart(request):
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    cart[id] = cart.get(id, quantity)

    request.session['cart'] = cart

    messages.success(request, "Product added to your cart")
    return redirect(reverse('allproducts')) # make it just reload page user is on?

def edit_cart(request, id):
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[id] = quantity
    else: 
        cart.pop(id)

    request.session['cart'] = cart

    messages.success(request, "Cart updated")
    return redirect(reverse('view_cart'))