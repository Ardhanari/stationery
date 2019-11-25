from django.shortcuts import render, redirect, reverse
from django.http import Http404
from .models import Product, ProductCategory

def all_products(request):
    """renders page with all available products, excluding these not available for buying"""
    products = Product.objects.all().exclude(quantity=0)
    return render(request, 'allproducts.html', {'products': products})

def single_product(request, id):
    """renders single product page with detailed information"""
    chosen_product = Product.objects.get(id=id)
    return render(request, 'singleproduct.html', {'chosen_product': chosen_product})

def product_category(request, category):
    """Renders category page with all the products belonging to it"""
    chosen_category = ProductCategory.objects.all().filter(name=category)
    productsfromcategory = Product.objects.all().filter(category=chosen_category)

    if not productsfromcategory:
        raise Http404()

    return render(request, 'productcategory.html', {'productsfromcategory': productsfromcategory, 'category': chosen_category})