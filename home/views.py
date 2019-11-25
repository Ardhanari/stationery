from django.shortcuts import render

# Create your views here.

def about(request):
    """Renders about page"""
    return render(request, 'about.html')

def faq(request):
    """Renders FAQ page"""
    return render(request, 'faq.html')