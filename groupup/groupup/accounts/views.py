from re import template
from django.shortcuts import render
from django.http    import HttpResponse
from .models import UserGroup
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .models import GroupUpUser
from django.contrib.auth.models import User
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(username = form.username, password = form.password)
            groupupuser = GroupUpUser(user, form.profile_pic, form.interests)
            groupupuser.save()


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
