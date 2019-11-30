from django.shortcuts import render
from products.models import Product, ProductCategory

def search_for_product(request):
    """
    Returns and renders search results based on the name of the product 
    """
    all_categories = ProductCategory.objects.all().distinct()
    query = request.GET['query']
    products = Product.objects.filter(name__icontains=request.GET['query'])
    return render(request, 'searchresults.html', {'products': products, 'query': query, 'all_categories': all_categories})
