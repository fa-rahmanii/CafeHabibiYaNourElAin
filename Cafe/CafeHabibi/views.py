from django.shortcuts import render

# Create your views here.

def home_page(request):
    
    # products = 
    return render(request, "index.html", {})

def login_page(request):
    return render(request, 'login_page.html', {})

def signup_page(request):
    return render(request, 'signup_page.html', {})

def products_page(request):
    pass