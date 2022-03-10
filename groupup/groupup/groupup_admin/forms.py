from django import forms
from groupup.accounts.widgets import DatePickerInput
from groupup.accounts.models import UserGroup

class AddAvailableDateForm(forms.Form):
    """  """
    date = forms.DateField(label='date', widget=DatePickerInput)

class RemoveDate(forms.Form):
    """  """
    date = forms.ModelChoiceField(queryset=None)
    
    def __init__(self, group, *args, **kwargs):
        super(RemoveDate, self).__init__(*args, **kwargs)
        self.fields["date"].queryset = group.connected_group.all()




class HandleRequestForm(forms.Form):
    """Form for handling a match request, uses radio buttons."""

    CHOICES = [('confirmed', 'Accept'), ('rejected', 'Decline')]
    status = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class InviteUserForm(forms.Form):
    """Form for inviting a user"""

    username = forms.CharField(max_length=30, label="Username")
    