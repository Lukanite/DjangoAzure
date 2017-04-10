"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
#from django.contrib import messages
#from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

#from .forms import MessageForm

from django.template import loader

from app.forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required



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


<<<<<<< HEAD
# def messages(request):
#     """Renders the messaging page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/message.html',
#         context_instance = RequestContext(request,
#                                          {
#                                               'title': 'Messages Home',
#                                               'year':datetime.now().year,
#                                           })
#     )
#
# @csrf_exempt
# def compose(request):
#     """Renders the new message page."""
#     #assert isinstance(request, HttpRequest)
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             print("Is valid")
#             # subject = request.POST.get('subject')
#             # content = request.POST.get('content')
#             # receiver = request.POST.get('receiver')
#             # message_obj = Message(subject=subject, content=content, sender=sender, receiver=receiver)
#             # message_obj.save()
#             form.sender = request.user
#             print (request.user)
#             form.save()
#            #  message_obj = Message(sender=sender)
#            #  message_obj.save()
#            # # Message.sender = request.user
#            # message = form.save()
#         else:
#             print("not valid")
#             print (form.errors)
#             render(request, 'app/compose.html', {'form' : form})
#         return render(request, 'app/outbox.html')
#     form = MessageForm()
#     print("not post")
#     return render(request, 'app/compose.html', {'form' : form}
#     )
#
#
# def inbox(request):
#     """Renders the inbox page."""
#     assert isinstance(request, HttpRequest)
#     message_list = Message.objects.inbox_for(request.user)
#     return render(
#         request,
#         'django_messages/inbox.html',
#         context_instance = RequestContext(request,
#         {
#             'title':'Your Inbox',
#             'message':'inbox',
#             'year':datetime.now().year,
#             'message_list' : message_list,
#         })
#     )
#
# def new_messages(request):
#     """Renders the new message notification page."""
#     assert isinstance(request, HttpRequest)
#
#     return render(
#         request,
#         'app/new_messages.html',
#         context_instance=RequestContext(request,
#                                         {
#                                             'title': 'Your new messages',
#                                             'message': 'new messages',
#                                             'year': datetime.now().year,
#                                         }))
#
#
# def outbox(request, username):
#     """Renders the outbox (sent messages) page."""
#     assert isinstance(request, HttpRequest)
#     # 'message_list'
#     #
#     # try:
#     #     user = User.objects.get(username=username)
#     # except:
#     #     raise Http404("Requested user not found.")
#     #
#     # template = get_template('app/outbox.html')
#     # variables = Context({'username: username'})
#     # output = template.render(variables)
#     # return HttpResponse(output)
#
#
#     # results = Message.objects.all()
#     # context = {'results': results}
#     # return render(request, 'app/outbox.html', context)
#
#     Sent = Message.objects.get(id=id)
#     message_data = {
#         "sender":Sent
#     }
#
#     print (message_data)
#
#     return render(
#         request,
#         'app/outbox.html', message_data,
#         context_instance = RequestContext(request,
#         {
#             'message_list':message_data,
#             'title':'Your outbox',
#             'message':'outbox',
#             'year':datetime.now().year,
#         })
#     )
#
# def trash(request):
#     """Renders the signup page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/trash.html',
#         context_instance = RequestContext(request,
#         {
#             'title':'your trash',
#             'message':'trash',
#             'year':datetime.now().year,
#         })
#     )
#
# def view(request):
#     """Renders the signup page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/view.html',
#         context_instance = RequestContext(request,
#         {
#             'title':'View',
#             'message':'single message',
#             'year':datetime.now().year,
#         })
#     )
=======
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
            'title': 'your trash',
            'message': 'trash',
            'year': datetime.now().year,
        }
    )


@login_required()
def view(request):
    """Renders the trash page."""
    assert isinstance(request, HttpRequest)
<<<<<<< HEAD
    if request.user.is_authenticated():
        return render(
            request,
            'app/view.html',
            context={
                'title': 'View',
                'message': 'single message',
                'year': datetime.now().year,
            }
        )
    else:
        return HttpResponseRedirect('/')

def group(request):
    """Renders the groups page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated():
        return render(
            request,
            'app/group.html',
            context={
                'title': 'Your Groups',
                'year': datetime.now().year,
            }
        )
    else:
        return HttpResponseRedirect('/')

def create_group(request):
    """Renders the new group page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated():
        return render(
            request,
            'app/create_group.html',
            context={
                'title': 'Create a Group',
                'year': datetime.now().year,
            }
        )
    else:
        return HttpResponseRedirect('/')

def userlist(request):
    context = RequestContext(request)
    if request.method == 'GET':
        users = UserForm(request.GET)
        user = User.objects.all()
    else:
        pass
    return render(request, 'create_group.html', {'user': user})
=======
    return render(
        request,
        'app/view.html',
        context={
            'title': 'View',
            'message': 'single message',
            'year': datetime.now().year,
        }
    )
>>>>>>> a3ee4f84bc3441b848062370224974556d073291
>>>>>>> 6c40b30979eda0741e9ab15b44a5f3b521ecfacb
