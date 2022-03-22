from django.test import TestCase
from groupup.accounts.tests import create_user, setup_group
from .models import Invite, Matches

class MatchesTest(TestCase):
    """Test the Matches model."""
    
    def test_constructor(self):
        admin1 = create_user("arnolf")
        admin2 = create_user("ulfstad")
        group1 = setup_group("arnolf", "ManBearPig")
        group2 = setup_group("ulfstad", "Sotuh Path")

        match = Matches.objects.create(requestor=group1, receiver=group2)

        self.assertEqual(match.requestor, group1)
        self.assertEqual(match.receiver, group2)
        self.assertEqual(match.status, "pending")
        self.assertFalse(match.have_met)

        match.status = "confirmed"
        match.save()
        self.assertEqual(match.status, "confirmed")

        match.have_met = True
        match.save()
        self.assertTrue(match.have_met)


class InviteTest(TestCase):
    """Test for the Invite model."""

    def test_constructor(self):
        user = create_user("wolfram")
        admin = create_user("amadeus")
        group = setup_group("amadeus", "Mozart")

        invite = Invite.objects.create(group=group, receiver=user)
        self.assertEqual(invite.group, group)
        self.assertEqual(invite.receiver, user)
        self.assertEqual(invite.status, "pending")

        invite.status = "rejected"
        invite.save()
        self.assertEqual(invite.status, "rejected")
