from django.db import models
from django.contrib.auth.models import User



def user_image_path(instance, filename):
    user_name = instance.user.username
    extension = filename.rsplit('.', 1)[1]
    return 'users/{0}.{1}'.format(user_name, extension)

class Interest(models.Model):
    name = models.CharField(max_length=30)

class GroupUpUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to = user_image_path)
    interests = models.ManyToManyField(Interest)

