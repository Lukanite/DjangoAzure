from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def is_site_manager(user):
    return user.profile.user_type == "site_manager"


@login_required()
@user_passes_test(is_site_manager, login_url='/', redirect_field_name="")
@csrf_exempt
def manage_users(request):
    assert isinstance(request, HttpRequest)
    users = User.objects.all()

    if (request.POST.get('suspend')):
        suspended_user = request.POST.get('suspend')
        suspended_user = users.get(username=suspended_user)
        suspended_user.is_active = False
        suspended_user.save()

    if (request.POST.get('restore')):
        suspended_user = request.POST.get('restore')
        suspended_user = users.get(username=suspended_user)
        suspended_user.is_active = True
        suspended_user.save()

    if (request.POST.get('promote')):
        promoted_user = request.POST.get('promote')
        promoted_user = users.get(username=promoted_user)
        promoted_user.profile.user_type = "site_manager"
        promoted_user.save()

    return render(
        request, 'site_manager/manage_users.html',
        {
            'title': 'Manage Users', 'message': 'Suspend or Promote Users',
            'year': datetime.now().year, 'users': users
        }
    )
