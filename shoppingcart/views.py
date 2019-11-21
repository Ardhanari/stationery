from django.shortcuts import render, redirect, reverse

def view_cart(request):
    """Renders the cart contents page """
    return render(request, "cart.html")

def add_to_cart(request):
    # if request.user.is_authenticated:
        return redirect(reverse('allproducts'))
    # else: 
        # return redirect(reverse('allproducts'))
