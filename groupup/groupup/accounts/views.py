from re import template
from django.shortcuts import render
from django.http    import HttpResponse


# Create your views here.
def register(request):
    print(request.POST.get)
    return render(request, "registration/registerForm.html")

    # Create your views here.
def index(request):
    return render(request, "groupup/accounts/templates/registration/index.html")