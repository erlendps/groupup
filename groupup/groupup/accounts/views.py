from re import template
from django.forms import ValidationError
from django.shortcuts import render
from django.http    import HttpResponse, HttpResponseRedirect
from .models import Interest, UserGroup
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .models import GroupUpUser
from django.contrib.auth.models import User
from .forms import RegisterForm

# Create your views here.
def register(request):
    """View for handling new groupupusers
    
    Checks if request method is POST. If the form is valid it creats a new user and groupupuser.
    If request method i GET it returns a empty form.
    """

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            if len(User.objects.filter(username=data.get("username"))) != 0:
                raise ValidationError(
                    ("Username already taken"),
                    code = "username_taken"
                )
            
            user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
            user.save()
            groupupuser = GroupUpUser(user=user, profile_pic=data.get("profile_pic"),birthday=data.get("birthday"))
            groupupuser.save()
            for interest in list(data.get("interests")):
                groupupuser.interests.add(interest.id)
            groupupuser.save()
            print(data.get("interests"))

            return HttpResponseRedirect('/home')

    else:
        form = RegisterForm()
        return render(request, 'registration/registerForm.html', {'form': form})

# Create your views here.
def index(request):
    return render(request, "groupup/accounts/templates/registration/index.html")
    
def homepage(request):
    return render(request, "accounts/home.html")

@login_required
def group_site(request, pk):
    group = UserGroup.objects.get(pk=pk)
    context = {"group": group}
    return render(request, "accounts/group_site.html", context)
