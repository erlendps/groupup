from numbers import Number
from posixpath import split
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import Interest, UserGroup
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from .models import GroupUpUser, UserGroup
from .forms import RegisterForm, GroupCreateForm
from django.contrib.auth.models import User
from groupup.groupup_admin.models import Invite
from django.db.models.functions import Lower


def homepage(request):
    """Renders the homepage for the user."""
    
    try:
        groups = request.user.groupupuser.get_groups()
        context = {"groups": groups}
        return render(request, "accounts/home.html", context)

    except AttributeError:
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

            return HttpResponseRedirect('/')

    else:
        form = RegisterForm()
    return render(request, 'registration/registerForm.html', {'form': form})


@login_required
def all_groups(request):
    """Renders a page with all groups."""
    
    allInterests = list(Interest.objects.all().order_by(Lower('name'), 'pk'))
    filteredInterests = request.GET.get("interests")

    groups = list(UserGroup.objects.all().order_by(Lower('name'), 'pk'))
    result = []
    if filteredInterests is None or len(filteredInterests) == 0:
        result = groups
    else:
        for group in groups:
            if set([int(x) for x in filteredInterests.split(',')]).issubset(set([int(x.pk) for x in group.interests.all()])):
                result.append(group)
    return render(request, "accounts/all_groups.html", {"groups": result, "interests": allInterests})

@login_required
def group_site(request, pk):
    """Renders the group site of the group with primary key pk."""

    group = UserGroup.objects.get(pk=pk)
    context = {"group": group}
    return render(request, "accounts/group_site.html", context)

@login_required
def remove_group_member(request, pk, user_id):
    group = UserGroup.objects.get(pk=pk)
    if group not in request.user.groupupuser.get_groups_where_admin():
        return HttpResponse('Unauthorized', status=401)
    
    user_to_delete = User.objects.get(pk=user_id)
    group.members.remove(user_to_delete.groupupuser)
    group.save()


@login_required
def group_matches(request, pk):
    """Renders a list of groups in which the group with primary key pk has a confirmed match with."""
    
    group = UserGroup.objects.get(pk=pk)
    if group not in request.user.groupupuser.get_groups():
        return Http404
    
    confirmed_groups = group.get_confirmed_groups()
    context = {
        "confirmed_groups": confirmed_groups,
        "usergroup": group
    }

    return render(request, "accounts/group_matches.html", context)


@login_required
def show_invites(request):
    user = request.user.groupupuser
    pending_invites = user.get_pending_invitations()

    context = {"pending_invites": pending_invites}

    return render(request, "accounts/show_invites.html", context)


@login_required
def accept_invite(request, pk):
    group = UserGroup.objects.get(pk=pk)
    user = request.user.groupupuser
    
    if user in group.get_members():
        raise Http404
    
    invitation = Invite.objects.get(group=group, receiver=user, status="pending")
    invitation.status = "confirmed"
    invitation.save()
    group.members.add(user)
    group.save()

    return HttpResponseRedirect("/profile/invites")


@login_required
def decline_invite(request, pk):
    group = UserGroup.objects.get(pk=pk)
    user = request.user.groupupuser
    
    if user in group.get_members():
        raise Http404
    
    invitation = Invite.objects.get(group=group, receiver=user, status="pending")
    invitation.status = "rejected"
    invitation.save()

    return HttpResponseRedirect("/profile/invites")