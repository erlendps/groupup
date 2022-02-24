from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from groupup.accounts.models import UserGroup
from groupup.group_matching.models import Matches
from .forms import HandleRequestForm


@login_required
def group_browsing(request, pk):
    """View for group site that has some extra functionality for the admin."""

    if not request.user.groupupuser.is_a_group_admin():
        return redirect("/groups/{0}".format(pk))
    request.session["pp_groupbrowsing"] = True
    request.session["group_pk"] = pk
    group = UserGroup.objects.get(pk=pk)
    context = {"group": group}
    return render(request, "group_matching/group_site_admin.html", context)


@login_required
def send_match_request(request, pk):
    """Sends a match requests based on the session cookie group_pk.
    
    Does a few checks, for instance, it checks that the admin in fact is matching
    on behalf of a group he is admin of. It also checks if there is already a relation
    between the two groups. If all checks pass, a new match request is created.
    """

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
        return redirect("/admin/group/{0}".format(receiver_group.id))
    else:
        raise Http404

@login_required
def view_match_requests(request, pk):
    """Returns a view with a list of all groups that has requested a match with the group with primary_key=pk."""
    if not request.user.groupupuser.is_a_group_admin():
        return redirect("/groups/{0}".format(pk))
    group = UserGroup.objects.get(pk=pk)
    # check if user is actually admin of requestor_group
    if group not in request.user.groupupuser.get_groups_where_admin():
        raise Http404
    request.session['pp_viewmatches'] = True
    request.session['group_pk'] = pk
    
    # get matches (and therefore groups) where the status is pending
    requesting_groups = []
    matches = group.get_matches(True)
    for match in matches:
        if match.status == 'pending':
            requesting_groups.append(match.requestor)
    context = {'requesting_groups': requesting_groups, 'groupname': group.name}
    return render(request, 'group_matching/match_requests.html', context)

@login_required
def handle_match_request(request, pk):
    """Handle a match request, e.g accept or decline.
    
    Creates a HandleRequestForm, and renders it. If the input is valid,
    the status will be set according to the POST-request.
    """
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
                match.save()
                return HttpResponseRedirect('/admin/viewmatchrequests/{0}'.format(receiving_group.id))
        else:
            form = HandleRequestForm()
        context = {'group': requesting_group, 'form': form}
        return render(request, 'group_matching/group_site_handle_request.html', context)
