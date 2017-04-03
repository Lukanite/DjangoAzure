"""
Definition of urls for DjangoApp.
"""

from datetime import datetime
from django.conf.urls import include, url
from app.forms import BootstrapAuthenticationForm
from app.views import *
from app.models import *
from reports.views import reportlist
from django.contrib.auth.views import *


# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
     
    url(r'^$', home, name='home'),
    url(r'^contact$', contact, name='contact'),
    url(r'^about', about, name='about'),
    url(r'^login/$', login, {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$', logout, {  'next_page': '/'  },        name='logout'),
    url(r'^signup', signup, name='signup'),
    url(r'^reports$', reportlist, name='reports'),
    url(r'^reports/', include('reports.urls')),
    url(r'^message', message, name='message'),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^compose', compose, name='compose'),
    url(r'^inbox', inbox, name='inbox'),
    url(r'^new_messages', new_messages, name='new_messages'),
    url(r'^outbox', outbox, name='outbox'),
    url(r'^trash', trash, name='trash'),
    url(r'^view', view, name='view'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
