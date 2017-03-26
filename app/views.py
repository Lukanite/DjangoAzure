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

def signup(request):
    """Renders the signup page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/signup.html',
        context_instance = RequestContext(request,
        {
            'title':'Sign up',
            'message':'Please Enter Your Information',
            'year':datetime.now().year,
        })
    )

@csrf_exempt
def submit_signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        context = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password': password,
            'user_type': user_type,
        }

        return render(
            request,
            'app/submit_signup.html',
            context_instance=RequestContext(request, context))
    else:
        template = loader.get_template('app/signup.html')
        return HttpResponse(template.render())




