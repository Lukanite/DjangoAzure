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
from django.http import HttpResponse, Http404
from app.forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
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

            return render(request, 'app/index.html', context_instance = RequestContext(request, {
                'title':'Home Page',
                'year':datetime.now().year,  }))
    else:
        user_form = UserForm()
        user_profile_form = ProfileForm()


    return render(request, 'app/signup.html', {'title':'Sign up',
                                           'message':'Please Enter Your Information',
                                           'year':datetime.now().year, 'user_form': user_form, 'user_profile_form' : user_profile_form})

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
