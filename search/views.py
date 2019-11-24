from django.shortcuts import render
from products.models import Product

def search_for_product(request):
    query = request.GET['query']
    products = Product.objects.filter(name__icontains=request.GET['query'])
    return render(request, 'searchresults.html', {'products': products, 'query': query})
