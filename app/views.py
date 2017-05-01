"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

#from .forms import MessageForm

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from app.forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import smtplib
#from .models import Message
#from django_messages import views
# from django_messages.models import Message
# from django_messages.forms import ComposeForm
# from django_messages.utils import format_quote, get_user_model, get_username_field




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
        request,
        'app/contact.html',
        context={
            'title': 'Contact',
            'message': 'Group 19 Contact Information',
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
            'message': 'Lokahi lets you succeed',
            'year': datetime.now().year,
        }
    )


# @csrf_exempt
# def login(request):
#     assert isinstance(request, HttpRequest)
#     captcha = CaptchaField()
#     return render(
#         request,
#         'app/login.html',
#         context={ 'title':'Log in',
#                 'year':datetime.now().year,
#                 'captcha':captcha
#         }
#     )

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
            send_signup_email(request.POST.get("user-first_name"), request.POST.get("user-last_name"), request.POST.get("user-email"))
            return HttpResponseRedirect('/')
    else:
        user_form = UserForm(prefix="user")
        user_profile_form = ProfileForm(prefix="profile")

    return render(
        request, 'app/signup.html',
        {
            'title': 'Sign up', 'message': 'Please Enter Your Information',
            'year': datetime.now().year, 'user_form': user_form,
            'user_profile_form': user_profile_form
        }
    )


@login_required()
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


@login_required()
def compose(request):
    """Renders the new message page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # new_message = Message.objects.create()
            subject = request.POST.get('subject', '')
            content = request.POST.get('content', '')
            sender = request.user
            receiver = request.POST.get('receiver', '')
            message_obj = Message(subject=subject, content=content)
            message_obj.save()
            return HttpResponseRedirect('new_messages')
    else:
        form = MessageForm
    return render(
        request,
        'app/compose.html',
        context={
            'title': 'New Message',
            'message': 'Write a new message',
            'year': datetime.now().year,
        }
    )


@login_required()
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


@login_required()
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


@login_required()
def outbox(request):
    """Renders the outbox page."""
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


@login_required()
def trash(request):
    """Renders the signup page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/trash.html',
        context={
            'title': 'Your trash',
            'message': 'trash',
            'year': datetime.now().year,
        }
    )


@login_required()
def view(request):
    """Renders the view page."""
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

def send_signup_email(firstname, lastname, recipient):


    gmail_user = "lokahiteam19"
    gmail_pwd = "cs3240lokahi"
    FROM = "Lokahi Fintech"
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = "Thank you for Signing Up!"
    TEXT = "Thank you " + firstname + " " + lastname + " for signing up to use Lokahi Fintech!"

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()
