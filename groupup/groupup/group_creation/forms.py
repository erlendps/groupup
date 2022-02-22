from unittest.util import _MAX_LENGTH
from django import forms

class GroupCreateForm(forms.Form):
    group_name = forms.CharField(label="group_name", max_length=100)
    group_description = forms.CharField(label="group_description", max_length=250)
    group_picture = forms.ImageField(label="group_picture")