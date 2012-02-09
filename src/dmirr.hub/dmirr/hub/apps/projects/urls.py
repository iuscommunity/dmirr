
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dmirr.hub.apps.projects.views',
    url(r'^$', 'list', name='list_projects'),
    url(r'^manage/$', 'manage', name='manage_projects'),
    url(r'^create/$', 'create', name='create_project'),
    url(r'^(?P<project>[\w\-\.\_]+)/$', 'show', name='show_project'),
    url(r'^(?P<project>[\w\-\.\_]+)/update/$', 'update', name='update_project'),
    url(r'^(?P<project>[\w\-\.\_]+)/delete/$', 'delete', name='delete_project'),
    url(r'^(?P<project>[\w\-\.\_]+)/repos/$', 'list_repos', name='list_project_repos'),
    url(r'^(?P<project>[\w\-\.\_]+)/repos/create/$', 'create_repo', name='create_project_repo'),
    url(r'^(?P<project>[\w\-\.\_]+)/repos/(?P<repo>[\w\-\.\_]+)/$', 'show_repo', name='show_project_repo'),
    url(r'^(?P<project>[\w\-\.\_]+)/repos/(?P<repo>[\w\-\.\_]+)/update/$', 'update_repo', name='update_project_repo'),
    url(r'^(?P<project>[\w\-\.\_]+)/repos/(?P<repo>[\w\-\.\_]+)/delete/$', 'delete_repo', name='delete_project_repo'),
    )