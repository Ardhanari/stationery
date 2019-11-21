from django.shortcuts import render

def view_cart(request):
    """Renders the cart contents page """
    return render(request, "cart.html")