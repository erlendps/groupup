import datetime
from dateutil.relativedelta import relativedelta
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
        """Sets up data used throughout the tests."""

        gaming = Interest.objects.create(name="Gaming")
        user = create_user("Matias")
        admin = create_user("Morten")
        basic = create_user("inga")
        userGroup = UserGroup.objects.create(name="SuicideSquad",
                                            description="Vi elsker suicide-shots",
                                            group_pic=img,
                                            group_admin=admin,
                                            admin_contact="example@gmail.com")
        userGroup.interests.add(gaming)
        userGroup.members.add(user)
        userGroup.members.add(admin)
    
    def test_constructor(self):
        """Tests that the constructor has the correct fields."""

        user = create_user("adminman")
        photo = Interest.objects.create(name="Photos")
        group = UserGroup.objects.create(name="PhotoManiacs",
                                        description="We are the maniacs",
                                        group_pic=img,
                                        group_admin=user)
        group.members.add(user)
        group.interests.add(photo)

        self.assertEqual(group.name, "PhotoManiacs")
        self.assertEqual(group.description, "We are the maniacs")
        self.assertEqual(group.group_admin, user)
        self.assertEqual(group.admin_contact, "example@gmail.com")
        self.assertEqual(list(group.members.all()), [user])
        self.assertEqual(list(group.interests.all()), [photo])

    def test_get_members(self):
        """Tests the get_members function by checking if members are in the list or not."""

        matias = GroupUpUser.objects.get(user=User.objects.get(username="Matias"))
        morten = GroupUpUser.objects.get(user=User.objects.get(username="Morten"))
        inga = GroupUpUser.objects.get(user=User.objects.get(username="inga"))
        group = UserGroup.objects.get(name="SuicideSquad")

        self.assertTrue(matias in list(group.get_members()))
        self.assertTrue(morten in list(group.get_members()))
        self.assertFalse(inga in list(group.get_members()))    

    def test_num_of_members(self):
        """Tests the number of members function."""

        group = UserGroup.objects.get(name="SuicideSquad")
        self.assertEqual(group.num_of_members(), 2)

    def test_get_age_gap(self):
        """Tests the age gap function.
        
        Uses relativedelta so that we dont have to update the test each year.
        """

        age1 = abs(relativedelta(datetime.date(2001, 4, 3), datetime.date.today()).years)
        age2 = abs(relativedelta(datetime.date(1998, 4, 3), datetime.date.today()).years)
        # everyone same age
        group = UserGroup.objects.get(name="SuicideSquad")
        self.assertEqual(group.get_age_gap(), "Everyone is {0} years old".format(age1))

        # different ages
        morten = GroupUpUser.objects.get(user=User.objects.get(username="Morten"))
        morten.birthday = datetime.date(1998, 4, 3)
        morten.save()
        self.assertEqual(group.get_age_gap(), "Ages from {0} to {1}".format(age1, age2))
        
    def test_get_three_interests(self):
        """Tests that the method correctly fetches 3 interests."""

        group = UserGroup.objects.get(name="SuicideSquad")
        gaming = Interest.objects.get(name="Gaming")
        hangover = Interest.objects.create(name="Hangovers")
        movies = Interest.objects.create(name="Movies")
        dogs = Interest.objects.create(name="Dogs")
        # only 1 interest
        self.assertEqual(group.get_three_interests(), [gaming])
        
        # 3 interests, should be in lexiographic order
        group.interests.add(hangover)
        group.interests.add(movies)
        self.assertEqual(group.get_three_interests(), [gaming, hangover, movies])

        # 4 interests, should include the three first in lexiographic order
        group.interests.add(dogs)
        self.assertEqual(group.get_three_interests(), [dogs, gaming, hangover])

    def test_matching_for_group(self):
        """Tests the methods related to matching with groups."""

        # create two groups
        ola = create_user("ola")
        donald = create_user("donald")
        beer = setup_group("ola", "beermen")
        wine = setup_group("donald", "Winemen")

        group = UserGroup.objects.get(name="SuicideSquad")

        # at first group should have no matches
        self.assertEqual(list(group.get_related_groups()), [])

        # create match where group is requestor
        match1 = Matches.objects.create(requestor=group, receiver=beer)
        self.assertEqual(list(group.get_related_groups()), [beer])
        self.assertTrue(beer in group.get_matchreceiving_groups())
        self.assertFalse(beer in group.get_matchrequesting_groups())
        # should now have a relation
        self.assertTrue(group.has_relation_with(beer))

        # create match where group is receiver
        match2 = Matches.objects.create(requestor=wine, receiver=group)
        self.assertTrue(wine in group.get_related_groups())
        self.assertFalse(wine in group.get_matchreceiving_groups())
        self.assertTrue(wine in group.get_matchrequesting_groups())

        #confirm match 1
        match1.status = "confirmed"
        match1.save()
        self.assertEqual(group.get_confirmed_groups(), [beer])

        # set have_met
        match1.have_met = True
        match1.save()
        # confirmed grups should now be empty
        self.assertEqual(group.get_confirmed_groups(), [])
        # and there should not be a relation between the groups
        self.assertFalse(group.has_relation_with(beer))

    def test_get_reviews(self):
        """Tests the get reviews function."""

        # create a review
        group = UserGroup.objects.get(name="SuicideSquad")
        review1 = Reviews.objects.create(group=group, review="They are funny yes")
        self.assertEqual(group.get_reviews(), [review1])
        review2 = Reviews.objects.create(group=group, review="They are not funny yes")
        self.assertTrue(review2 in group.get_reviews())

