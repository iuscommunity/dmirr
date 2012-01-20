
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dmirr.hub.apps.protocols.views',
    url(r'^$', 'index', name='protocols_index'),
    url(r'^create/$', 'create', name='create_protocol'),
    url(r'^(?P<protocol>[\w]+)/$', 'show', name='show_protocol'),
    url(r'^(?P<protocol>[\w]+)/update/$', 'update', name='update_protocol'),
    url(r'^(?P<protocol>[\w]+)/delete/$', 'delete', name='delete_protocol'),
    )