
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dmirr.hub.apps.archs.views',
    url(r'^$', 'list', name='list_archs'),
    url(r'^manage/$', 'manage', name='manage_archs'),
    url(r'^create/$', 'create', name='create_arch'),
    url(r'^(?P<arch>[\w]+)/$', 'show', name='show_arch'),
    url(r'^(?P<arch>[\w]+)/update/$', 'update', name='update_arch'),
    url(r'^(?P<arch>[\w]+)/delete/$', 'delete', name='delete_arch'),
    )