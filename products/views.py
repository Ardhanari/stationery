from django.shortcuts import render, redirect, reverse
from .models import Product

def all_products(request):
    """renders page with all available products, excluding these not available for buying"""
    products = Product.objects.all().exclude(quantity=0)
    return render(request, 'allproducts.html', {'products': products})

def single_product(request, id):
    """renders single product page with detailed information"""
    chosen_product = Product.objects.get(id=id)
    return render(request, 'singleproduct.html', {'chosen_product': chosen_product})