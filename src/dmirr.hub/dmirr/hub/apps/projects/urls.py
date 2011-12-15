from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('dmirr.hub.apps.projects.views',
    url(r'^$', 'index'),
    url(r'^create/', 'create', name='create_project'),
    url(r'^(?P<pk>[\d]+)/$', 'display', name='display_project'),
    url(r'^(?P<pk>[\d]+)/update/$', 'update', name='update'),
    url(r'^(?P<pk>[\d]+)/delete/$', 'delete', name='delete_project'),
    )