from django import forms
from groupup.accounts.widgets import DatePickerInput
from datetime import date as dt


def validate_date(date):
    if date < dt.today():
        raise forms.ValidationError("%s is before today".format(date))

class AddAvailableDateForm(forms.Form):
    """  """
    date = forms.DateField(label='Date to add', widget=DatePickerInput, validators=[validate_date])

class RemoveDate(forms.Form):
    """  """
    date = forms.ModelChoiceField(label='Date to remove', queryset=None)
    
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


class ReviewForm(forms.Form):
    """"Form for wiriting reviews"""
    
    review = forms.CharField(max_length = 280, label = "Review")
    
    