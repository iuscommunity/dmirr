
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dmirr.hub.apps.projects.views',
    url(r'^$', 'list', name='list_projects'),
    url(r'^manage/$', 'manage', name='manage_projects'),
    url(r'^create/$', 'create', name='create_project'),
    url(r'^(?P<project>[\w\-\.\_]+)/$', 'show', name='show_project'),
    url(r'^(?P<project>[\w\-\.\_]+)/update/$', 'update', name='update_project'),
    url(r'^(?P<project>[\w\-\.\_]+)/delete/$', 'delete', name='delete_project'),
    )