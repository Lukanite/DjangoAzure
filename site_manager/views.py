from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

def is_site_manager(user):
    return user.profile.user_type == "site_manager"

@login_required()
@user_passes_test(is_site_manager, login_url='/', redirect_field_name = "")
def site_manager(request):
    assert isinstance(request, HttpRequest)
    users = User.objects.all()
    return render(
            request, 'site_manager/site_manager.html',
            {
                'title': 'Site Manager', 'message': 'This Page is only for site managers',
                'year': datetime.now().year, 'users': users
            }
    )

# @csrf_exempt
# def signup(request):
#     """Renders the signup page."""
#     if request.method == "POST":
#         user_form = UserForm(request.POST, prefix="user")
#         user_profile_form = ProfileForm(request.POST, prefix="profile")
#         if user_form.is_valid() and user_profile_form.is_valid():
#             new_user = User.objects.create_user(**user_form.cleaned_data)
#             user_type = request.POST.get("profile-user_type")
#             new_user.profile.user_type = user_type
#             new_user.save()
#             username = request.POST.get('user-username')
#             password = request.POST.get('user-password')
#             new_user = authenticate(username=username, password=password)
#             login(request, new_user)
#             return HttpResponseRedirect('/')
#     else:
#         user_form = UserForm(prefix="user")
#         user_profile_form = ProfileForm(prefix="profile")
#
#     return render(
#         request, 'app/signup.html',
#         {
#             'title': 'Sign up', 'message': 'Please Enter Your Information',
#             'year': datetime.now().year, 'user_form': user_form,
#             'user_profile_form': user_profile_form
#         }
#     )