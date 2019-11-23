from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

def view_cart(request):
    """Renders the cart contents page """
    return render(request, "cart.html")

def add_to_cart(request, id):
    # current_page = request.path_info # it gets url for add_to_cart. I need URL of the page it was launched from :|
    previous_url = request.META.get('HTTP_REFERER')
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    
    if id in cart:
        cart[id] = int(cart[id]) + quantity      
    else:
        cart[id] = cart.get(id, quantity) 

    request.session['cart'] = cart

    messages.success(request, "Product added to your cart")
    # return redirect(reverse('viewcart')) # make it just reload page user is on?
    # return HttpResponseRedirect(request.path_info)
    # return HttpResponseRedirect("")
    return redirect(previous_url)
    # return redirect(reverse(current_page))

def edit_cart(request, id):
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[id] = quantity
    else: 
        cart.pop(id)

    request.session['cart'] = cart

    messages.success(request, "Cart updated")
    return redirect(reverse('viewcart'))