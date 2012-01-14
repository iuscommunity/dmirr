
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dmirr.hub.apps.repos.views',
    url(r'^(?P<project>[\w\-\.\_]+)/repos/$', 'index', name='repos_index'),
    url(r'^(?P<project>[\w\-\.\_]+)/repos/create/$', 'create', name='create_repo'),
    url(r'^(?P<project>[\w\-\.\_]+)/repos/(?P<repo>[\w\-\.\_]+)/$', 'show', name='show_repo'),
    url(r'^(?P<project>[\w\-\.\_]+)/repos/(?P<repo>[\w\-\.\_]+)/update/$', 'update', name='update_repo'),
    url(r'^(?P<project>[\w\-\.\_]+)/repos/(?P<repo>[\w\-\.\_]+)/delete/$', 'delete', name='delete_repo'),
    )