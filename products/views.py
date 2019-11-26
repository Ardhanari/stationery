from django.shortcuts import render, redirect, reverse
from django.http import Http404
from .models import Product, ProductCategory

def all_products(request):
    """renders page with all available products, excluding these not available for buying"""
    all_categories = ProductCategory.objects.all().distinct()
    print(all_categories) #sanity check
    products = Product.objects.all().exclude(quantity=0)

    # SORTING - if method was POST then the results will be sorted accordingly
    if request.method == 'POST':
        if request.POST['sort'] == 'price-low-to-high':
            productsfromcategory = Product.objects.all().filter(category=chosen_category).order_by('-price')
        elif request.POST['sort'] == 'price-high-to-low':
            productsfromcategory = Product.objects.all().filter(category=chosen_category).order_by('price')
        elif request.POST['sort'] == 'date-new-first':
            productsfromcategory = Product.objects.all().filter(category=chosen_category).order_by('-created_at')
        elif request.POST['sort'] == 'date-old-first':
            productsfromcategory = Product.objects.all().filter(category=chosen_category).order_by('created_at')
        else:
            messages.warning("Something went wrong with sorting products!")

    return render(request, 'allproducts.html', {'products': products, 'all_categories': all_categories})

def single_product(request, id):
    """renders single product page with detailed information"""
    chosen_product = Product.objects.get(id=id)
    return render(request, 'singleproduct.html', {'chosen_product': chosen_product})

def product_category(request, category):
    """Renders category page with all the products belonging to it"""
    all_categories = ProductCategory.objects.all().distinct()

    try:
        chosen_category = ProductCategory.objects.get(name=category)
        productsfromcategory = Product.objects.all().filter(category=chosen_category)
    except:
        raise Http404()

    # SORTING - if method was POST then the results will be sorted accordingly
    if request.method == 'POST':
        if request.POST['sort'] == 'price-low-to-high':
            productsfromcategory = Product.objects.all().filter(category=chosen_category).order_by('-price')
        elif request.POST['sort'] == 'price-high-to-low':
            productsfromcategory = Product.objects.all().filter(category=chosen_category).order_by('price')
        elif request.POST['sort'] == 'date-new-first':
            productsfromcategory = Product.objects.all().filter(category=chosen_category).order_by('-created_at')
        elif request.POST['sort'] == 'date-old-first':
            productsfromcategory = Product.objects.all().filter(category=chosen_category).order_by('created_at')
        else:
            messages.warning("Something went wrong with sorting products!")

    return render(request, 'productcategory.html', {'productsfromcategory': productsfromcategory, 'category': chosen_category, 'all_categories': all_categories})