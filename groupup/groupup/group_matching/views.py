from multiprocessing import context
from django.dispatch import receiver
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from groupup.accounts.models import UserGroup
from groupup.group_matching.models import Matches
from .forms import HandleRequestForm


@login_required
def group_browsing(request, pk):
    if not request.user.groupupuser.is_a_group_admin():
        return redirect("/groups/{0}".format(pk))
    request.session["pp_groupbrowsing"] = True
    request.session["group_pk"] = pk
    group = UserGroup.objects.get(pk=pk)
    context = {"group": group}
    return render(request, "group_matching/group_site_admin.html", context)

@login_required
def send_match_request(request, pk):
    if "pp_groupbrowsing" in request.session:
        requestor_group = UserGroup.objects.get(pk=pk)
        receiver_group = UserGroup.objects.get(pk=request.session.get("group_pk"))
        # check if group is itself
        if requestor_group == receiver_group:
            del request.session["pp_groupbrowsing"]
            raise Http404
        # check if user is actually admin of requestor_group
        if requestor_group not in request.user.groupupuser.get_groups_where_admin():
            del request.session["pp_groupbrowsing"]
            raise Http404
        # check if theres already a relation between the groups
        if requestor_group.has_relation_with(receiver_group):
            del request.session["pp_groupbrowsing"]
            raise Http404
        
        # everything good, create match
        match = Matches(requestor=requestor_group, receiver=receiver_group)
        match.save()
        del request.session["pp_groupbrowsing"]
        return redirect("/matching/group/{0}".format(receiver_group.id))
    else:
        raise Http404

@login_required
def view_match_requests(request, pk):
    if not request.user.groupupuser.is_a_group_admin():
        return redirect("/groups/{0}".format(pk))
    group = UserGroup.objects.get(pk=pk)
    # check if user is actually admin of requestor_group
    if group not in request.user.groupupuser.get_groups_where_admin():
        raise Http404
    request.session['pp_viewmatches'] = True
    request.session['group_pk'] = pk
    requesting_groups = group.get_matchrequesting_groups()
    context = {'requesting_groups': requesting_groups}
    return render(request, 'group_matching/match_requests.html', context)

@login_required
def handle_match_request(request, pk):
    if 'pp_viewmatches' in request.session:
        requesting_group = UserGroup.objects.get(pk=pk)
        receiving_group = UserGroup.objects.get(pk=request.session.get('group_pk'))
        if not request.user.groupupuser.is_admin_of(receiving_group):
            del request.session['pp_viewmatches']
            raise Http404
        if request.method == 'POST':
            form = HandleRequestForm(request.POST)
            if form.is_valid():
                status = form.cleaned_data['status']
                match = Matches.objects.get(requestor=requesting_group, receiver=receiving_group)
                match.status = status
                return HttpResponseRedirect('matching/viewmatchrequests/{0}'.format(receiving_group.id))
        else:
            form = HandleRequestForm()
        context = {'group': requesting_group, 'form': form}
        return render(request, 'group_matching/group_site_handle_request.html', context)
