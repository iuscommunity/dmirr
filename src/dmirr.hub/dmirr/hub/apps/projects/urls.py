
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('dmirr.hub.apps.projects.views',
    url(r'^$', 'index', name='projects_index'),
    url(r'^create/', 'create', name='create_project'),
    url(r'^(?P<project_id>[\d]+)/$', 'show', name='show_project'),
    url(r'^(?P<project_id>[\d]+)/update/$', 'update', name='update_project'),
    url(r'^(?P<project_id>[\d]+)/delete/$', 'delete', name='delete_project'),
    )