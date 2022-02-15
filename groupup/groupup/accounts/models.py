from pyexpat import model
from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User
import datetime
from dateutil.relativedelta import relativedelta



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
    """Represents a user who uses 
    
    Has a one to one relation to Django's predefined user model
    and has other fields as well
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to = user_image_path, blank=True)
    interests = models.ManyToManyField(Interest, blank=True)
    birthday = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'groupupuser'
    
    def __str__(self):
        return self.user.username


def group_image_path(instance, filename):
    group_name = instance.name
    pk_string = instance.id
    extension = filename.rsplit('.', 1)[1]
    return 'groups/{0}_{1}.{2}'.format(group_name, pk_string, extension)


class UserGroup(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    num_of_members = models.IntegerField(default=1)
    interests = models.ManyToManyField(Interest, blank=True)
    group_pic = models.ImageField(upload_to=group_image_path, blank=True)
    members = models.ManyToManyField(GroupUpUser)
    group_admin = models.ForeignKey(GroupUpUser, on_delete=models.CASCADE, related_name="group_admin")

    class Meta:
        db_table = 'user_group'

    def get_age_gap(self):
        today = datetime.date.today()
        youngest = datetime.date(1900, 1, 1)
        oldest = datetime.date(2100, 1, 1)
        for member in self.members.all():
            if member.birthday > youngest:
                youngest = member.birthday
            if member.birthday < oldest:
                oldest = member.birthday
        return "{0}-{1}".format(abs(relativedelta(youngest, today).years), abs(relativedelta(oldest, today).years))
    
    def __str__(self):
        return self.name
        