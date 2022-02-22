from django.shortcuts import render
from django.http    import Http404
from .models import UserGroup
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, "accounts/home.html")

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
