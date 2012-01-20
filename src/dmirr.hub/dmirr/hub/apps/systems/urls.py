
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dmirr.hub.apps.systems.views',
    url(r'^$', 'index', name='systems_index'),
    url(r'^create/$', 'create', name='create_system'),
    url(r'^(?P<system>[\w\-\_\.]+)/$', 'show', name='show_system'),
    url(r'^(?P<system>[\w\-\_\.]+)/update/$', 'update', name='update_system'),
    url(r'^(?P<system>[\w\-\_\.]+)/delete/$', 'delete', name='delete_system'),
    )