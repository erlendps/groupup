from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from groupup.accounts.models import GroupUpUser, UserGroup, DateAvailable
from .models import Matches, Invite
from .forms import HandleRequestForm, InviteUserForm, AddAvailableDateForm, RemoveDate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.functions import Lower



@login_required
def admin_index(request):
    """Renders a page with all the groups the user is admin of."""

    if not request.user.groupupuser.is_a_group_admin():
        raise Http404

    groups = request.user.groupupuser.get_groups_where_admin()
    context = {"groups": groups}
    return render(request, "groupup_admin/admin_index.html", context)


@login_required
def all_groups(request):
    """Renders a page with all groups."""

    if not request.user.groupupuser.is_a_group_admin():
        raise Http404

    allInterests = list(Interest.objects.all().order_by(Lower('name'), 'pk'))
    filteredInterests = request.GET.get("interests")

    groups = list(UserGroup.objects.all().order_by(Lower('name'), 'pk'))
    result = []
    if filteredInterests is None or len(filteredInterests) == 0:
        result = groups
    else:
        for group in groups:
            if set(filteredInterests).issubset(set([str(x.pk) for x in group.interests.all()])):
                result.append(group)
    return render(request, "groupup_admin/all_groups.html", {"groups": result, "interests": allInterests})


@login_required
def group_browsing(request, pk):
    """View for group site that has some extra functionality for the admin.
    
    Sets some cookies based on the site and also handles the invite user.
    """

    if not request.user.groupupuser.is_a_group_admin():
        return redirect("/groups/{0}".format(pk))
    request.session["pp_groupbrowsing"] = True
    request.session["group_pk"] = pk
    group = UserGroup.objects.get(pk=pk)

    # form handling
    if request.method == "POST":
        invite_form = InviteUserForm(request.POST)
        if invite_form.is_valid():
            user = None
            try:
                user = GroupUpUser.objects.get(user=User.objects.get(username=invite_form.cleaned_data.get("username")))
                if user.is_member_of_group(group):
                    messages.warning(request, "User already a member")
                elif user.has_pending_invite(group):
                    messages.warning(request, "Already invited user")
                else:
                    invite = Invite.objects.create(group=group, receiver=user)
                    invite.save()
                    messages.success(request, "Successfully invited the user!")

            except:
                messages.warning(request, "User does not exist.")
            invite_form = InviteUserForm()
            return HttpResponseRedirect(request.path)
    else:
        invite_form = InviteUserForm()
    add_date = AddAvailableDateForm()
    remove_date = RemoveDate(group)

    context = {
        "group": group,
        "invite_form": invite_form,
        "add_date": add_date,
        "remove_date": remove_date,
    }
    return render(request, "groupup_admin/group_site_admin.html", context)


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

        # give feedback
        messages.success(request, "Sent a match request!")
        del request.session["pp_groupbrowsing"]
        return redirect("/admin/groups/{0}".format(receiver_group.id))
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
    return render(request, 'groupup_admin/match_requests.html', context)

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
                if status == "confirmed":
                    messages.success(request, "You have matched with {0}".format(requesting_group.name))
                else:
                    messages.success(request, "You declined {0}'s match request".format(requesting_group.name))
                return HttpResponseRedirect('/admin/viewmatchrequests/{0}'.format(receiving_group.id))
        else:
            form = HandleRequestForm()
        context = {'group': requesting_group, 'form': form}
        return render(request, 'groupup_admin/group_site_handle_request.html', context)

def add_date(request, pk):
    if request.method == 'POST':
        add_date_form = AddAvailableDateForm(request.POST)
        if add_date_form.is_valid():
            group = UserGroup.objects.get(pk=pk)
            date = add_date_form.cleaned_data['date']
            if len(DateAvailable.objects.filter(group=group, date=date))!=0:
                return redirect("/admin/groups/{0}".format(pk))
            date_available = DateAvailable(group=group, date=date)
            date_available.save()
            return HttpResponseRedirect("/admin/groups/{0}".format(pk))
        else:
            return redirect("/admin/groups/{0}".format(pk))
    else:
        return redirect("/admin/groups/{0}".format(pk))


def remove_date(request, pk):
    if request.method == "POST":
        group = UserGroup.objects.get(pk=pk)
        remove_date_form = RemoveDate(group, request.POST)
        if remove_date_form.is_valid():
            group = UserGroup.objects.get(pk=pk)
            date = remove_date_form.cleaned_data['date']
            date.delete()
            return HttpResponseRedirect("/admin/groups/{0}".format(pk))
    else:
        return redirect("/admin/groups/{0}".format(pk))