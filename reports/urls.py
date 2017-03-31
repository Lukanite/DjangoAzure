from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.detail, name='index'),
    url(r'^new$', views.newreport, name='new'),
    url(r'^(?P<report_id>[0-9]+)/$', views.detail, name='detail'),
]