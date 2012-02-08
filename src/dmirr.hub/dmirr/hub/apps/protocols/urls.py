
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dmirr.hub.apps.protocols.views',
    url(r'^$', 'list', name='list_protocols'),
    url(r'^manage/$', 'manage', name='manage_protocols'),
    url(r'^create/$', 'create', name='create_protocol'),
    url(r'^(?P<protocol>[\w]+)/$', 'show', name='show_protocol'),
    url(r'^(?P<protocol>[\w]+)/update/$', 'update', name='update_protocol'),
    url(r'^(?P<protocol>[\w]+)/delete/$', 'delete', name='delete_protocol'),
    )