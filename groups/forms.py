"""
Definition of forms.
"""
import re
from django import forms
from django.contrib.auth.models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

    def clean_name(self):
        data = self.cleaned_data['name']
        pattern = re.compile('([^\s\w]|_)+')
        data = pattern.sub('', data)
        return data
