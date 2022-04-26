from django.db import models
from django.core.validators import RegexValidator


class Matches(models.Model):
    """Represents a relation between two groups.
    
    Has a requestor, a receiver and a status that can be either rejected, pending (defualt)
    or confirmed. A match also has a "have_met" field that keeps track on wheter the two groups
    have met or not.
    """
    
    requestor = models.ForeignKey("accounts.UserGroup", on_delete=models.CASCADE, related_name='match_requestor')
    receiver = models.ForeignKey("accounts.UserGroup", on_delete=models.CASCADE, related_name='match_receiver')
    status = models.CharField(max_length=10, default="pending" ,validators=[RegexValidator(regex="(rejected|pending|confirmed)$",
                                message="Must be one of the following: rejected, pending or confirmed")])
    have_met = models.BooleanField(default=False)


    class Meta:
        db_table = "matches"

    def set_have_met(self):
        self.have_met = True

    def __str__(self):
        return "match_between_{0}_{1}".format(self.requestor.id, self.receiver.id)


class Invite(models.Model):
    """Small table representing a invite to a group."""

    group = models.ForeignKey("accounts.UserGroup", on_delete=models.CASCADE, related_name="group")
    receiver = models.ForeignKey("accounts.GroupUpUser", on_delete=models.CASCADE, related_name="receiver")
    status = models.CharField(max_length=10, default="pending" ,validators=[RegexValidator(regex="(rejected|pending|confirmed)$",
                                message="Must be one of the following: rejected, pending or confirmed")])


    def __str__(self):
        return "{0}_invite_{1}".format(self.group.name, self.receiver.user.username)

        
    class Meta:
        db_table = "invite"