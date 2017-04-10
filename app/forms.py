"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from app.models import Profile
from .models import Message


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
        model = Message
        exclude = ['sender']
        #fields = ('recipient', 'subject', 'content', 'sender',)

   # subject = forms.CharField(required=True, label='Message Subject')
    #message_body = forms.CharField(required=True, label='Message Body', widget=forms.Textarea)

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('url', 'user_type')

class UserForm(forms.ModelForm):
    class Meta:
        prefix = 'user'
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        prefix = 'profile'
        model = Profile
        # TYPES = ((0, 'Company_User'), (1, 'Investor_User'))
        # user_type = forms.TypedChoiceField(label='user_type', choices=TYPES, widget=forms.RadioSelect,)
        fields = ['user_type']






