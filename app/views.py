"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.http import HttpResponse
from app.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )

@csrf_exempt
def signup(request):
    """Renders the signup page."""
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            username = request.POST.get('username')
            password = request.POST.get('password')
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            # redirect, or however you want to get to the main view
            return render(request, 'app/index.html', context_instance = RequestContext(request, {
            'title':'Home Page',
            'year':datetime.now().year,  }))
    else:
        form = UserForm()

    return render(request, 'app/signup.html', {'title':'Sign up',
                                           'message':'Please Enter Your Information',
                                           'year':datetime.now().year, 'form': form})

def message(request):
    """Renders the messaging page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/message.html',
        context_instance = RequestContext(request,
                                         {
                                              'title': 'Messages Home',
                                              'year':datetime.now().year,
                                          })
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
        form = MessageForm()
    return render(
        request,
        'app/compose.html',
        context_instance = RequestContext(request,
        {
            'title':'New Message',
            'message':'Write a new message',
            'year':datetime.now().year,
        })
    )

def inbox(request):
    """Renders the inbox page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/inbox.html',
        context_instance = RequestContext(request,
        {
            'title':'Your Inbox',
            'message':'inbox',
            'year':datetime.now().year,
        })
    )

def new_messages(request):
    """Renders the new message notification page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/new_messages.html',
        context_instance=RequestContext(request,
                                        {
                                            'title': 'Your new messages',
                                            'message': 'new messages',
                                            'year': datetime.now().year,
                                        }))


def outbox(request):
    """Renders the signup page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/outbox.html',
        context_instance = RequestContext(request,
        {
            'title':'Your outbox',
            'message':'outbox',
            'year':datetime.now().year,
        })
    )

def trash(request):
    """Renders the signup page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/trash.html',
        context_instance = RequestContext(request,
        {
            'title':'your trash',
            'message':'trash',
            'year':datetime.now().year,
        })
    )

def view(request):
    """Renders the signup page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/view.html',
        context_instance = RequestContext(request,
        {
            'title':'View',
            'message':'single message',
            'year':datetime.now().year,
        })
    )
