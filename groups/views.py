from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from django.template import loader
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, Http404

from groups.forms import GroupForm
from django.contrib.auth.models import Group


@login_required()
def group(request):
    """Renders the groups page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'groups/group.html',
        context={
            'title': 'Your Groups',
            'year': datetime.now().year
        }
    )


@login_required()
@csrf_exempt
def create_group(request):
    """Renders the new group page."""
    if request.method == "POST":
        group_form = GroupForm(request.POST)
        if group.is_valid():
            new_group = Group.objects.create(group_form)
            new_group.save()
            return HttpResponseRedirect('/groups')
    return render(
        request,
        'groups/create_group.html',
        context={
            'title': 'Create a Group',
            'year': datetime.now().year,
        }
    )

def userlist(request):
    context = RequestContext(request)
    if request.method == 'GET':
        users = UserForm(request.GET)
        user = User.objects.all()
    else:
        pass
    return render(request, 'groups/create_group.html', {'user': user})
