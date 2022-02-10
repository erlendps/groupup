from re import template
from django.shortcuts import render
from django.http    import HttpResponse


# Create your views here.
def register(request):
    return render(request, "accounts/registerForm.html")

    # Create your views here.
def index(request):
    return render(request, "accounts/loginForm.html")