# from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from groupup.accounts.models import UserGroup
from groupup.group_creation.forms import GroupCreateForm
# from groupup.group_matching.models import Matches
# from .forms import HandleRequestForm


@login_required
def handle_create_group(request):
    """Handle a match request, e.g accept or decline.
    
    Creates a HandleRequestForm, and renders it. If the input is valid,
    the status will be set according to the POST-request.
    """
    print(request)
    if request.method == 'POST':
        form = GroupCreateForm(request.POST)
        # if form.is_valid():
        group = UserGroup.objects.create(name=form.group_name, description=form.group_description, group_pic=form.group_picture, group_admin=request.user.groupupuser)
        group.save()
        return HttpResponseRedirect('/accounts/groups/' + group.pk)
    else:
        form = GroupCreateForm()
    return render(request, "group_creation.html", {'form':form})
    # if not request.user.groupupuser.is_admin_of(receiving_group):
    #     del request.session['pp_viewmatches']
    #     raise Http404
    # if request.method == 'POST':
    #     form = HandleRequestForm(request.POST)
    #     if form.is_valid():
    #         status = form.cleaned_data['status']
    #         match = Matches.objects.get(requestor=requesting_group, receiver=receiving_group)
    #         match.status = status
    #         match.save()
    #         return HttpResponseRedirect('/admin/viewmatchrequests/{0}'.format(receiving_group.id))
    # context = {'group': requesting_group, 'form': form}
    # return render(request, 'group_matching/group_site_handle_request.html', context)