from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.db import ProgrammingError
from .models import Product, ProductCategory, ProductReview

def all_products(request):
    """renders page with all available products, excluding these not available for buying"""
    all_categories = ProductCategory.objects.all().distinct()
    products = Product.objects.all().exclude(quantity=0)

    # SORTING - if method was POST then the results will be sorted accordingly
    if request.method == 'POST':
        if request.POST['sort'] == 'price-low-to-high':
            products = Product.objects.all().exclude(quantity=0).order_by('price')
        elif request.POST['sort'] == 'price-high-to-low':
            products = Product.objects.all().exclude(quantity=0).order_by('-price')
        elif request.POST['sort'] == 'date-new-first':
            products = Product.objects.all().exclude(quantity=0).order_by('-created_at')
        elif request.POST['sort'] == 'date-old-first':
            products = Product.objects.all().exclude(quantity=0).order_by('created_at')
        else:
            messages.warning(request, "Something went wrong with sorting products!")

    return render(request, 'allproducts.html', {'products': products, 'all_categories': all_categories})

def single_product(request, id):
    """renders single product page with detailed information"""
    chosen_product = Product.objects.get(id=id)
    try: 
        product_reviews = ProductReview.objects.all().filter(product=chosen_product)
    except:
        product_reviews = []

    return render(request, 'singleproduct.html', {'chosen_product': chosen_product, 'reviews': product_reviews})

def product_category(request, category):
    """Renders category page with all the products belonging to it"""
    all_categories = ProductCategory.objects.all().distinct()

    try:
        chosen_category = ProductCategory.objects.get(name=category)
        productsfromcategory = Product.objects.all().exclude(quantity=0).filter(category=chosen_category)
    except:
        raise Http404()

    # SORTING - if method was POST then the results will be sorted accordingly
    if request.method == 'POST':
        if request.POST['sort'] == 'price-low-to-high':
            productsfromcategory = Product.objects.all().exclude(quantity=0).filter(category=chosen_category).order_by('price')
        elif request.POST['sort'] == 'price-high-to-low':
            productsfromcategory = Product.objects.all().exclude(quantity=0).filter(category=chosen_category).order_by('-price')
        elif request.POST['sort'] == 'date-new-first':
            productsfromcategory = Product.objects.all().exclude(quantity=0).filter(category=chosen_category).order_by('-created_at')
        elif request.POST['sort'] == 'date-old-first':
            productsfromcategory = Product.objects.all().exclude(quantity=0).filter(category=chosen_category).order_by('created_at')
        else:
            messages.warning(request, "Something went wrong with sorting products!")

    return render(request, 'productcategory.html', {'productsfromcategory': productsfromcategory, 'category': chosen_category, 'all_categories': all_categories})