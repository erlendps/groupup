from re import template
from django.shortcuts import render
from django.http    import HttpResponse
from .models import UserGroup
from django.contrib.auth.decorators import login_required


# Create your views here.
def homepage(request):
    return render(request, "accounts/home.html")

@login_required
def group_site(request, pk):
    group = UserGroup.objects.get(pk=pk)
    context = {"group": group}
    return render(request, "accounts/group_site.html", context)