import datetime
from sqlite3 import Date
from django.test import TestCase
from .models import Interest, Reviews, GroupUpUser, UserGroup, DateAvailable
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)
img = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')

def create_user(username):
    user = GroupUpUser.objects.create(user=User.objects.create(username=username),
                                profile_pic=img,
                                birthday=datetime.date(2001, 4, 3))
    return user

def setup_group(username, groupname):
    groupupuser = GroupUpUser.objects.get(user=User.objects.get(username=username))
    group = UserGroup.objects.create(name=groupname,
                                description="Blah Blah",
                                group_pic=img,
                                group_admin=groupupuser
    )
    group.members.add(groupupuser)
    return group


class InterestTest(TestCase):
    def setUp(self):
        Interest.objects.create(name="Music")
        Interest.objects.create(name="Sport")
    
    def test_interest_get_correct_name(self):
        music = Interest.objects.get(name="Music")
        sport = Interest.objects.get(name="Sport")
        
        self.assertEqual(music.name, "Music")
        self.assertEqual(sport.name, "Sport")


class DateAvailableTest(TestCase):
    def setUp(self):
        user = create_user("promp")
        group = setup_group("promp", "friends")
        DateAvailable.objects.create(date=datetime.date(2022, 1, 16), group=group) 
        DateAvailable.objects.create(date=datetime.date(2022, 8, 9), group=group)

    def test_constructor(self):
        group = UserGroup.objects.get(name="friends")
        date1 = DateAvailable.objects.get(date=datetime.date(2022, 1, 16))
        date2 = DateAvailable.objects.get(date=datetime.date(2022, 8, 9))

        self.assertEqual(date1.group, group)
        self.assertEqual(date1.date, datetime.date(2022, 1, 16))
        self.assertEqual(date2.date, datetime.date(2022, 8, 9))