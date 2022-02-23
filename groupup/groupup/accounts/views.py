from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.http import Http404, HttpResponseRedirect
from .models import UserGroup
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from .models import GroupUpUser, UserGroup
from .forms import RegisterForm, GroupCreateForm
from django.contrib.auth.models import User


def homepage(request):
    return render(request, "accounts/home.html")

class UserGroupCreateView(LoginRequiredMixin, FormView):
    """View for creating new groups."""

    http_method_names = ['get', 'post']
    form_class = GroupCreateForm
    template_name = "accounts/group_creation.html"

    def form_valid(self, form: GroupCreateForm):
        obj = form.save(self.request.user.groupupuser)
        self.success_url = obj.get_absolute_url()
        return super().form_valid(form)

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

@login_required
def group_site(request, pk):
    """Renders the group site of the group with primary key pk."""

    group = UserGroup.objects.get(pk=pk)
    context = {"group": group}
    return render(request, "accounts/group_site.html", context)


@login_required
def group_matches(request, pk):
    """Renders a list of groups in which the groupw with primary key pk has a confirmed match with."""
    
    group = UserGroup.objects.get(pk=pk)
    if group not in request.user.groupupuser.get_groups():
        return Http404
    
    confirmed_groups = group.get_confirmed_groups()
    context = {
        "confirmed_groups": confirmed_groups,
        "usergroup": group
    }

    return render(request, "accounts/group_matches.html", context)