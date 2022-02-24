from django import forms

class HandleRequestForm(forms.Form):
    """Form for handling a match request, uses radio buttons."""

    CHOICES = [('confirmed', 'Accept'), ('rejected', 'Decline')]
    status = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class InviteUserForm(forms.Form):
    """Form for inviting a user"""

    username = forms.CharField(max_length=30, label="Username")
    