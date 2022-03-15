from django.db import models
from django.contrib.auth.models import User
import datetime
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from groupup.groupup_admin.models import Invite, Matches



def user_image_path(instance, filename):
    """Produces the file path to the users profile picture"""

    user_name = instance.user.username
    extension = filename.rsplit('.', 1)[1]
    return 'users/{0}.{1}'.format(user_name, extension)


class Interest(models.Model):
    """Represents an interest i.e. sport or music"""

    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'interest'

    def __str__(self):
        return self.name


class GroupUpUser(models.Model):
    """Represents a user who uses the app
    
    Has a one to one relation to Django's predefined user model
    and has other fields as well
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to = user_image_path, blank=True)
    interests = models.ManyToManyField(Interest, blank=True)
    birthday = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'groupupuser'
    

    def is_a_group_admin(self):
        """Returns true if the user is a group admin."""

        return len(self.get_groups_where_admin()) > 0

    def get_groups(self):
        """Returns a list of all groups the user is connected to."""

        return list(self.usergroup_set.all().order_by('name', 'pk'))
    
    def get_groups_where_admin(self):
        """Returns a list of all groups where the user is admin."""

        groups = []
        for group in self.get_groups():
            if self == group.group_admin:
                groups.append(group)
        return groups

    def is_admin_of(self, group):
        """Returns true if the user is the group admin of the given group."""

        return self == group.group_admin

    def is_member_of_group(self, group):
        """Returns true if this user is a member of the given group."""

        return self in group.members.all()

    def get_pending_invitations(self):
        """Returns a list of pending group invitations."""
        
        return list(self.receiver.filter(status="pending"))

    def has_pending_invite(self, group):
        """Returns true if user has a pending invite with the given group."""

        if Invite.objects.filter(receiver=self, group=group, status="pending"):
            return True
        return False

    def __str__(self):
        return self.user.username


def group_image_path(instance, filename):
    """Returns a path for the image for a group."""

    group_name = instance.name
    pk_string = instance.id
    extension = filename.rsplit('.', 1)[1]
    return 'groups/{0}_{1}.{2}'.format(group_name, pk_string, extension)


class UserGroup(models.Model):
    """Represents a group.
    
    A group has multiple fields, such as name, description. It has a many to many relation
    to GroupUpUsers and a special field (group_admin), which is a one to many field.
    """

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    interests = models.ManyToManyField(Interest, blank=True)
    group_pic = models.ImageField(upload_to=group_image_path, blank=True)
    members = models.ManyToManyField(GroupUpUser)
    group_admin = models.ForeignKey(GroupUpUser, on_delete=models.CASCADE, related_name="group_admin")

    class Meta:
        db_table = 'user_group'
        permissions = (
            ("group_admin", "Create and respond to group matches"), # probably can be removed
        )


    def get_members(self):
        """Returns a list of members of the group."""
        
        return list(self.members.all())

    def num_of_memers(self):
        """Returns the number of members in this group."""

        return len(self.members.all())

    def get_age_gap(self):
        """Returns the age gap in a group, represented as a string."""

        today = datetime.date.today()
        youngest = datetime.date(1900, 1, 1)
        oldest = datetime.date(2100, 1, 1)
        for member in self.members.all():
            if member.birthday > youngest:
                youngest = member.birthday
            if member.birthday < oldest:
                oldest = member.birthday

        if youngest == oldest:
            return "Everyone is {0} years old".format(abs(relativedelta(youngest, today).years))

        return "Ages from {0} to {1}".format(abs(relativedelta(youngest, today).years), abs(relativedelta(oldest, today).years))

    def get_three_interests(self):
        """Returns a list of 3 interests."""

        return list(self.interests.all().order_by('name', 'pk')[:3])

    def get_matches(self, is_receiver):
        """Returns a list of matches where either the group is the receiver or requestor of a match request."""

        if is_receiver:
            return list(Matches.objects.filter(receiver=self))
        return list(Matches.objects.filter(requestor=self))

    def get_matchrequesting_groups(self):
        """Returns a list of groups that has requested a match with self."""

        received_matches = self.get_matches(True)
        requestors = []

        for match in received_matches:
            requestors.append(match.requestor)
        return requestors
    
    def get_matchreceiving_groups(self):
        """Returns a list of groups that has received a match request from self."""

        requested_matches = self.get_matches(False)
        receivers = []

        for match in requested_matches:
            receivers.append(match.receiver)
        return receivers

    def get_confirmed_groups(self):
        """Returns a list of groups that self has a confirmed match with."""
        
        confirmed_groups = []
        for match in self.get_matches(True):
            if match.status == "confirmed":
                confirmed_groups.append(match.requestor)
        for match in self.get_matches(False):
            if match.status == "confirmed":
                confirmed_groups.append(match.receiver)
        
        return confirmed_groups

    def get_related_groups(self):
        """Finds all groups that are related, i.e there is a record in matches table containg this group."""

        return self.get_matchreceiving_groups() + self.get_matchrequesting_groups()

    def has_relation_with(self, group):
        """Returns true if self has a relation with the given group."""

        received_matches = list(Matches.objects.filter(receiver=self, requestor=group))
        requested_matches = list(Matches.objects.filter(receiver=group, requestor=self))
        return len(received_matches+requested_matches) != 0

    def get_absolute_url(self):
        return reverse('accounts:group_site', kwargs={'pk': self.pk})
        
    
    def __str__(self):
        return self.name
        