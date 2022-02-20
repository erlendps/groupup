from random import choices
from django import forms

class HandleRequestForm(forms.Form):
    """Form for handling a match request, uses radio buttons."""

    CHOICES = [('confirmed', 'Accept'), ('rejected', 'Decline')]
    status = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    