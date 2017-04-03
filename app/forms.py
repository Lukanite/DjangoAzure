"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from .models import Messages

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class MessageForm(forms.ModelForm):

    class Meta:
        model = Messages
        fields = ('subject', 'content',)

   # subject = forms.CharField(required=True, label='Message Subject')
    #message_body = forms.CharField(required=True, label='Message Body', widget=forms.Textarea)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('url', 'user_type')
