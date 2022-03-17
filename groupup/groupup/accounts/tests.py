import datetime
from django.test import TestCase
from .models import Interest, Reviews, GroupUpUser, UserGroup, DateAvailable
from groupup.groupup_admin.models import Invite, Matches
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)
img = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')

def create_user(username):
    """Creates a simple GroupUpUser."""

    user = GroupUpUser.objects.create(user=User.objects.create(username=username),
                                profile_pic=img,
                                birthday=datetime.date(2001, 4, 3))
    return user

def setup_group(username, groupname):
    """Creates a new UserGroup with name groupname and groupadmin username."""

    groupupuser = GroupUpUser.objects.get(user=User.objects.get(username=username))
    group = UserGroup.objects.create(name=groupname,
                                description="Blah Blah",
                                group_pic=img,
                                group_admin=groupupuser
    )
    group.members.add(groupupuser)
    return group


class InterestTest(TestCase):
    """Test Interest model."""

    def setUp(self):
        Interest.objects.create(name="Music")
        Interest.objects.create(name="Sport")
    
    def test_interest_get_correct_name(self):
        """Test that the name is set correctly."""

        music = Interest.objects.get(name="Music")
        sport = Interest.objects.get(name="Sport")
        
        self.assertEqual(music.name, "Music")
        self.assertEqual(sport.name, "Sport")


class DateAvailableTest(TestCase):
    """Test DateAvailable model."""

    def setUp(self):
        user = create_user("promp")
        group = setup_group("promp", "friends")
        DateAvailable.objects.create(date=datetime.date(2022, 1, 16), group=group) 
        DateAvailable.objects.create(date=datetime.date(2022, 8, 9), group=group)

    def test_constructor(self):
        """Test the constructor and checks that every field is set correctly when creating
        a new instance."""

        group = UserGroup.objects.get(name="friends")
        date1 = DateAvailable.objects.get(date=datetime.date(2022, 1, 16))
        date2 = DateAvailable.objects.get(date=datetime.date(2022, 8, 9))

        self.assertEqual(date1.group, group)
        self.assertEqual(date1.date, datetime.date(2022, 1, 16))
        self.assertEqual(date2.date, datetime.date(2022, 8, 9))


class ReviewsTest(TestCase):
    """Test Reviews model."""

    def setUp(self):
        user = create_user("Ola")
        group = setup_group("Ola", "ProggeSquad")
        Reviews.objects.create(group=group, review="6 av 6")
        Reviews.objects.create(group=group, review="5 av 6")
    
    def test_constructor(self):
        """Tests the constructor and that fields are set correctly."""

        group = UserGroup.objects.get(name="ProggeSquad")
        review1 = Reviews.objects.get(group=group, review="6 av 6")
        review2 = Reviews.objects.get(group=group, review="5 av 6")

        self.assertEqual(review1.group, group)
        self.assertEqual(review1.review, "6 av 6")
        self.assertEqual(review2.review, "5 av 6")


class GroupUpUserTest(TestCase):
    """Test GroupUpUser model."""

    def setUp(self):
        """Sets up data used in the test."""

        user = create_user("mainman")
        group = setup_group("mainman", "mainmen")
        justin = Interest.objects.create(name="JustinBieber")
        csgo = Interest.objects.create(name="CS:GO")
        user.interests.add(justin)
        user.interests.add(csgo)

        # basic user with no connections
        basic_user = create_user("petter")
    
    def test_constructor(self):
        """Tests the constructor.
        
        Creates a GroupUpUser objects and checks that fields are set correctly.
        Also checks that a GroupUpUser needs a User objects connected to it.
        """

        user = User.objects.create(username="bruhman")
        bday = datetime.date(2000, 5, 5)
        groupuser = GroupUpUser.objects.create(user=user,
                                                profile_pic=img,
                                                birthday=bday)
        groupuser.interests.add(Interest.objects.get(name="CS:GO"))
        
        self.assertEqual(groupuser.user, user)
        self.assertEqual(list(groupuser.interests.all()), [Interest.objects.get(name="CS:GO")])
        self.assertEqual(groupuser.birthday, bday)
        
        # test create GroupUpUser with no User connected                                                      birthday=bday))
        with self.assertRaises(ObjectDoesNotExist):
            GroupUpUser.objects.create(profile_pic=img,
                                       birthday=bday)

    def test_is_group_admin(self):
        """Tests the is_group_admin function."""

        group_admin = GroupUpUser.objects.get(user=User.objects.get(username="mainman"))
        basic_user = GroupUpUser.objects.get(user=User.objects.get(username="petter"))

        self.assertTrue(group_admin.is_a_group_admin())
        self.assertFalse(basic_user.is_a_group_admin())

    def test_get_groups(self):
        """Tests the get_groups function."""

        user = GroupUpUser.objects.get(user=User.objects.get(username="mainman"))
        basic_user = create_user("verybasic")
        group = UserGroup.objects.get(name="mainmen")

        self.assertEqual(user.get_groups(), [group])
        self.assertEqual(basic_user.get_groups(), [])
        group.members.add(basic_user)
        self.assertEqual(basic_user.get_groups(), [group])

    def test_get_groups_where_admin(self):
        """Tests the get_groups_where_admin function."""

        user = GroupUpUser.objects.get(user=User.objects.get(username="mainman"))
        basic_user = GroupUpUser.objects.get(user=User.objects.get(username="petter"))
        group = UserGroup.objects.get(name="mainmen")

        self.assertEqual(user.get_groups_where_admin(), [group])
        self.assertEqual(basic_user.get_groups_where_admin(), [])
        group.members.add(basic_user)
        self.assertEqual(basic_user.get_groups_where_admin(), [])
        group.members.remove(basic_user)

    def test_is_admin_of(self):
        """Tests the test_is_admin_of function."""

        user = GroupUpUser.objects.get(user=User.objects.get(username="mainman"))
        group = UserGroup.objects.get(name="mainmen")

        self.assertTrue(user.is_admin_of(group))
        basic_user = GroupUpUser.objects.get(user=User.objects.get(username="petter"))
        group.members.add(basic_user)
        self.assertFalse(basic_user.is_admin_of(group))
        group.members.remove(basic_user)  

    def test_is_member_of_group(self):
        """Tests the is_member_of_group function.

        Adds and removes a user to check that it correctly updates.
        """

        user = GroupUpUser.objects.get(user=User.objects.get(username="mainman"))
        basic_user = GroupUpUser.objects.get(user=User.objects.get(username="petter"))
        group = UserGroup.objects.get(name="mainmen")
        
        self.assertTrue(user.is_member_of_group(group))
        self.assertFalse(basic_user.is_member_of_group(group))
        
        group.members.add(basic_user)
        self.assertTrue(basic_user.is_member_of_group(group))
        group.members.remove(basic_user)

    def test_group_invitations(self):
        """Tests both the get_pending_invitations and has_pending_invite functions."""

        user = GroupUpUser.objects.get(user=User.objects.get(username="mainman"))
        basic_user = GroupUpUser.objects.get(user=User.objects.get(username="petter"))
        group = UserGroup.objects.get(name="mainmen")

        self.assertFalse(basic_user.has_pending_invite(group))
        self.assertEqual(basic_user.get_pending_invitations(), [])

        invite = Invite.objects.create(receiver=basic_user, group=group)
        self.assertTrue(basic_user.has_pending_invite(group))
        self.assertEqual(basic_user.get_pending_invitations(), [invite])
        invite.status = "confirmed"
        invite.save()
        self.assertFalse(basic_user.has_pending_invite(group))
        self.assertEqual(basic_user.get_pending_invitations(), [])


class UserGroupTest(TestCase):
    def setUp(self):
        gaming = Interest.objects.create(name="Gaming")
        user = create_user("Matias")
        admin = create_user("Morten")
        userGroup = UserGroup.objects.create(name="SuicideSquad",
                                            description="Vi elsker suicide-shots",
                                            group_pic=img,
                                            group_admin=admin,
                                            admin_contact="example@gmail.com")
        userGroup.interests.add(gaming)
        userGroup.members.add(user)
        userGroup.members.add(admin)
    
    def test_constructor(self):
        user = create_user