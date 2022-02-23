from django import forms
from groupup.accounts.models import UserGroup, GroupUpUser

class GroupCreateForm(forms.ModelForm):
    """A form used for creating new groups."""

    class Meta:
        model = UserGroup
        fields = ["name", "description", "group_pic"]

    def save(self, owner: GroupUpUser) -> UserGroup:
        """
        Creates a new instance of GroupUpUser and saves the result.
        """
        self.instance.group_admin = owner
        return super().save(commit=True)
