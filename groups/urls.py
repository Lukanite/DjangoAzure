from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.groups, name='index'),
    #url(r'^create_group$', views.create_group, name='create_group'),
    url(r'^(?P<name>[a-zA_Z0-9]+)/$', views.manage_users, name='manage_users'),
]