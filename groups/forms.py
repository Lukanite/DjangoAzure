"""
Definition of forms.
"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']