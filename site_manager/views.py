from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import smtplib



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
        text = "Hello, " + suspended_user.first_name + " " + suspended_user.last_name + ". This email is to notify you that your account access has been temporarily suspended. You will be unable to log into Lokahi related products until a Site Manager restores your account."
        send_email(suspended_user.email, "Account Suspension", text)

    if (request.POST.get('restore')):
        suspended_user = request.POST.get('restore')
        suspended_user = users.get(username=suspended_user)
        suspended_user.is_active = True
        suspended_user.save()
        text = "Hello, " + suspended_user.first_name + " " + suspended_user.last_name + ". This email is to notify you that your account access has been restored. You will be now be able to log into Lokahi related products."
        send_email(suspended_user.email, "Account Restored", text)

    if (request.POST.get('promote')):
        promoted_user = request.POST.get('promote')
        promoted_user = users.get(username=promoted_user)
        promoted_user.profile.user_type = "site_manager"
        promoted_user.save()
        text = "Hello, " + promoted_user.first_name + " " + promoted_user.last_name + ". This email is to notify you that your account has been promoted to Site Manager. You will be now be able to view/edit/delete all reports, manage all groups, and suspend/restore/promote other users!"
        send_email(promoted_user.email, "Account Promoted", text)


    return render(
        request, 'site_manager/manage_users.html',
        {
            'title': 'Manage Users', 'message': 'Suspend or Promote Users',
            'year': datetime.now().year, 'users': users
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

