from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from groupup.accounts.models import UserGroup, DateAvailable, Interest, Reviews
from .models import Matches
from .forms import HandleRequestForm, AddAvailableDateForm, RemoveDate, ReviewForm
from django.contrib import messages

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
        return redirect("/groups/{0}".format(receiver_group.id))
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
                match = Matches.objects.get(requestor=requesting_group, receiver=receiving_group, have_met = False)
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

@login_required
def add_date(request, pk):
    """Handles adding a date the group is available.
    
    Checks if the date is already added and redirects back to site if it is.
    """
    
    if request.method == 'POST':
        add_date_form = AddAvailableDateForm(request.POST)
        if add_date_form.is_valid():
            group = UserGroup.objects.get(pk=pk)
            date = add_date_form.cleaned_data['date']
            if len(DateAvailable.objects.filter(group=group, date=date))!=0:
                return redirect("/groups/{0}".format(pk))
            date_available = DateAvailable(group=group, date=date)
            date_available.save()
            #return HttpResponseRedirect("/admin/groups/{0}".format(pk))
            return HttpResponseRedirect("/groups/{0}".format(pk))
        else:
            #return redirect("/admin/groups/{0}".format(pk))
            return redirect("/groups/{0}".format(pk))
    else:
        #return redirect("/admin/groups/{0}".format(pk))
        return redirect("/groups/{0}".format(pk))

@login_required
def remove_date(request, pk):
    """Handles the removal of a available date for a group."""

    if request.method == "POST":
        group = UserGroup.objects.get(pk=pk)
        remove_date_form = RemoveDate(group, request.POST)
        if remove_date_form.is_valid():
            group = UserGroup.objects.get(pk=pk)
            date = remove_date_form.cleaned_data['date']
            date.delete()
            #return HttpResponseRedirect("/admin/groups/{0}".format(pk))
            return HttpResponseRedirect("/groups/{0}".format(pk))
    else:
        #return redirect("/admin/groups/{0}".format(pk))
        return redirect("/groups/{0}".format(pk))

@login_required
def have_met(request, pk):
    users_group = UserGroup.objects.get(pk=pk)
    group = UserGroup.objects.get(pk=request.session.get("group_pk"))

    match = list(Matches.objects.filter(receiver=users_group, requestor=group, have_met=False)) + list(Matches.objects.filter(receiver=group, requestor=users_group, have_met=False))
    print(match)
    if len(match) == 0 or len(match) > 1:
        return redirect("/groups/{0}".format(pk))
    match = match[0]
    match.have_met = True
    match.save()
    return redirect("/admin/groups/review/{0}".format(request.session.get("group_pk")))
    
@login_required
def write_review(request, pk):
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            group = UserGroup.objects.get(pk=pk)
            review = Reviews.objects.create(group=group, review=review_form.cleaned_data["review"])
            review.save()
            return HttpResponseRedirect("/groups/{0}".format(pk))
    else:
        form = ReviewForm()
        context = {'form': form}
        return render(request, "groupup_admin/review.html", context)


@login_required
def delete_group(request, pk):
    group = UserGroup.objects.get(pk=pk)
    if request.method == "POST":
        if "delete" in request.POST:
            if not request.user.groupupuser.is_admin_of(group):
                messages.warning("You are not administrator for this group!")
                return redirect("/admin/groups/{0}".format(pk))
            group.group_pic.delete(save=True)
            group.delete()
            return HttpResponseRedirect("/")
        else:
            return redirect("/admin/groups/{0}".format(pk))
    else:
        return render(request, "groupup_admin/delete_user.html", {"group": group})
