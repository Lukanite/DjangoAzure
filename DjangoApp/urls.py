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
from site_manager.views import site_manager
#File uploads
from django.conf import settings
from django.conf.urls.static import static

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
    # url(r'^messages$', messages, name='messages'),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^compose', compose, name='compose'),
    url(r'^inbox', inbox, name='inbox'),
    url(r'^new_messages', new_messages, name='new_messages'),
    url(r'^outbox', outbox, name='outbox'),
    url(r'^trash', trash, name='trash'),
    url(r'^view', view, name='view'),
    url(r'^group', group, name='group'),
    url(r'^create_group', create_group, name='create_group'),
    url(r'^site_manager$', site_manager, name='site_manager'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
