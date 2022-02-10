from django.db import models
from django.contrib.auth.models import User



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


class GroupUpUser(models.Model):
    """Represents a user who uses 
    
    Has a one to one relation to Django's predefined user model
    and has other fields as well
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to = user_image_path)
    interests = models.ManyToManyField(Interest)

    class Meta:
        db_table = 'groupupuser'

