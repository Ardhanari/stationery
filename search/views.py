from django.shortcuts import render
from products.models import products

def search_for_product(request):
    products = Product.object.filter(name__icontains=request.GET['q'])
    render(request, 'products.html', {'products': products})
