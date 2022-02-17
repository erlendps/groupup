from re import template
from django.shortcuts import render
from django.http    import HttpResponse
from .models import GroupUpUser

def homepage(request):
    return render(request, "accounts/home.html")

def group_site(request, pk):
    return render(request, "accounts/group_site.html")


# Create your views here.
def home(request):
    context = {
        'name': 'Matias',
    }
    return render(request, "accounts/home.html", context)

    