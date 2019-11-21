from django.shortcuts import render, redirect, reverse
from .models import Product

def all_products(request):
    products = Product.objects.all()
    return render(request, 'allproducts.html', {'products': products})

def add_to_cart(request):
    if request.user.is_authenticated:
        return
    else: 
        return redirect(reverse('allproducts'))
