"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from app.forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'index.html',
        context={
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        'app/contact.html',
        context={
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context={
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )


@csrf_exempt
def signup(request):
    """Renders the signup page."""
    if request.method == "POST":
        user_form = UserForm(request.POST, prefix="user")
        user_profile_form = ProfileForm(request.POST, prefix="profile")
        if user_form.is_valid() and user_profile_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            user_type = request.POST.get("profile-user_type")
            new_user.profile.user_type = user_type
            new_user.save()
            username = request.POST.get('user-username')
            password = request.POST.get('user-password')
            new_user = authenticate(username=username, password=password)
            login(request, new_user)

            return render(request, 'app/index.html', context={
                'title': 'Home Page',
                'year': datetime.now().year, })
    else:
        user_form = UserForm()
        user_profile_form = ProfileForm()

    return render(request, 'app/signup.html',
                  {
                      'title': 'Sign up', 'message': 'Please Enter Your Information',
                      'year': datetime.now().year, 'user_form': user_form,
                      'user_profile_form': user_profile_form
                  }
                  )


def message(request):
    """Renders the messaging page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/message.html',
        context={
            'title': 'Messages Home',
            'year': datetime.now().year,
        }
    )


def compose(request):
    """Renders the new message page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            subject = request.POST.get('subject', '')
            message_body = request.POST.get('message_body', '')
            return HttpResponseRedirect('new_messages')
    else:
        form = MessageForm(forms.FORM)
    return render(
        request,
        'app/compose.html',
        context={
            'title': 'New Message',
            'message': 'Write a new message',
            'year': datetime.now().year,
        }
    )


def inbox(request):
    """Renders the inbox page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/inbox.html',
        context={
            'title': 'Your Inbox',
            'message': 'inbox',
            'year': datetime.now().year,
        }
    )


def new_messages(request):
    """Renders the new message notification page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/new_messages.html',
        context={
                'title': 'Your new messages',
                'message': 'new messages',
                'year': datetime.now().year,
        }
    )


def outbox(request):
    """Renders the signup page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/outbox.html',
        context={
                'title': 'Your outbox',
                'message': 'outbox',
                'year': datetime.now().year,
        }
    )


def trash(request):
    """Renders the signup page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/trash.html',
        context={
            'title': 'your trash',
            'message': 'trash',
            'year': datetime.now().year,
        }
    )


def view(request):
    """Renders the signup page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/view.html',
        context={
            'title': 'View',
            'message': 'single message',
            'year': datetime.now().year,
        }
    )
