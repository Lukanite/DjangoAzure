from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from groups.forms import GroupForm
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
import smtplib


@login_required()
@csrf_exempt
def groups(request):
    assert isinstance(request, HttpRequest)
    groups = []
    other_groups = []
    for g in Group.objects.all():
        if request.user.groups.filter(name=g.name).exists():
            groups.append(g)
        else:
            other_groups.append(g)

    if request.POST.get('leave'):
        leave_group = Group.objects.get(name=request.POST.get('leave'))
        leave_group.user_set.remove(request.user)
        return HttpResponseRedirect('/groups')

    if request.POST.get('manage'):
        return HttpResponseRedirect('/groups/' + request.POST.get('manage'))

    return render(
        request, 'groups/group.html',
        {
            'title': 'Your Groups',
            'year': datetime.now().year,
            'groups': groups,
            'other_groups': other_groups
        }
    )


@login_required()
@csrf_exempt
def create_group(request):
    """Renders the new group page."""
    if request.method == "POST":
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            new_group = Group.objects.create(**group_form.cleaned_data)
            new_group.save()
            new_group.user_set.add(request.user)
            return HttpResponseRedirect('/groups')
    else:
        group_form = GroupForm()
    return render(
        request,
        'groups/create_group.html',
        context={
            'title': 'Create a Group',
            'year': datetime.now().year,
            'group_form': group_form,
        }
    )


@login_required()
@csrf_exempt
def group_users(request, name):
    users = User.objects.all()
    user_in_group = []
    user_not_in_group = []

    for u in users:
        if u != request.user and u.username != "admin":
            if u.groups.filter(name=name).exists():
                user_in_group.append(u)
            else:
                user_not_in_group.append(u)

    if request.POST.get('add'):
        group = Group.objects.get(name=name)
        user = User.objects.get(username=request.POST.get('add'))
        group.user_set.add(user)
        text = 'Hello, ' + user.first_name + '. This email is to notify you that you have been added to the "' + group.name + '" group! You can now view all reports associated with this group.'
        send_email(user.email, "You've been added to a new group", text)
        return HttpResponseRedirect('/groups/' + group.name)

    if request.POST.get('remove'):
        group = Group.objects.get(name=name)
        user = User.objects.get(username=request.POST.get('remove'))
        group.user_set.remove(user)
        text = 'Hello, ' + user.first_name + '. This email is to notify you that you have been removed from the "' + group.name + '" group. You can no longer view reports associated with this group.'
        send_email(user.email, "You've been removed from a group", text)
        return HttpResponseRedirect('/groups/' + group.name)

    return render(
        request,
        'groups/detail.html',
        context={
            'title': 'Manage Users in Group: ' + name,
            'year': datetime.now().year,
            'users': users,
            'user_in_group': user_in_group,
            'user_not_in_group': user_not_in_group
        }
    )

def send_email(recipient, subject, text):


    gmail_user = "lokahiteam19"
    gmail_pwd = "cs3240lokahi"
    FROM = "Lokahi Fintech"
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = text

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()