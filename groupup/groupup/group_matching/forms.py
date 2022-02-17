from random import choices
from django import forms

class HandleRequestForm(forms.Form):
    CHOICES = [('confirmed', 'Accept'), ('rejected', 'Decline')]
    status = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    