from django.shortcuts import render

def index(request):
    """Return index.html file"""

    return render(request, 'index.html')

def logout(request):
    return

def login(request):
    return

def register(request):
    return
    