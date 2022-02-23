from django.shortcuts import render
from django.http    import Http404
from groupup.accounts.forms import GroupCreateForm
from .models import UserGroup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

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
