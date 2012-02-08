
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dmirr.hub.apps.systems.views',
    url(r'^$', 'list', name='list_systems'),
    url(r'^manage/$', 'manage', name='manage_systems'),
    url(r'^create/$', 'create', name='create_system'),
    url(r'^(?P<system>[\w\-\_\.]+)/$', 'show', name='show_system'),
    url(r'^(?P<system>[\w\-\_\.]+)/update/$', 'update', name='update_system'),
    url(r'^(?P<system>[\w\-\_\.]+)/delete/$', 'delete', name='delete_system'),
    url(r'^(?P<system>[\w\-\_\.]+)/resources/create/$', 'create_resource', name='create_system_resource'),
    url(r'^(?P<system>[\w\-\_\.]+)/resources/(?P<resource>[\d]+)/$', 'show_resource', name='show_system_resource'),
    url(r'^(?P<system>[\w\-\_\.]+)/resources/(?P<resource>[\d]+)/update/$', 'update_resource', name='update_system_resource'),
    url(r'^(?P<system>[\w\-\_\.]+)/resources/(?P<resource>[\d]+)/delete/$', 'delete_resource', name='delete_system_resource'),
    )