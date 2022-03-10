from django import forms
from groupup.accounts.models import UserGroup, GroupUpUser
from .models import Interest
from .widgets import DatePickerInput

class InterestsWidget(forms.SelectMultiple):
    template_name="widgets/interests_widget.html"

class RegisterForm(forms.Form):
    """Form for creating a new groupupuser"""
    
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    profile_pic = forms.ImageField(label="profile_pic")
    interests = forms.ModelMultipleChoiceField(
                                    label="interests",
                                    queryset=Interest.objects.all(),
                                    widget=InterestsWidget)
    birthday = forms.DateField(label="dateofbirth", widget=DatePickerInput)

class GroupCreateForm(forms.ModelForm):
    """A form for creating new groups."""
    interests = forms.ModelMultipleChoiceField(
                                    label="Interests",
                                    queryset=Interest.objects.all(),
                                    widget=InterestsWidget)

    class Meta:
        model = UserGroup
        fields = ["name", "description", "group_pic", "admin_contact"]

    def save(self, owner: GroupUpUser) -> UserGroup:
        """
        Creates a new instance of GroupUpUser and saves the result.
        """
        self.instance.group_admin = owner
        self.instance.admin_contact = self.cleaned_data['admin_contact']
        returnValue = super().save(commit=True)
        self.instance.members.add(owner)
        for interest in self.cleaned_data['interests']:
            self.instance.interests.add(interest.id)
        return returnValue
