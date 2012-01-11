
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dmirr.hub.apps.distros.views',
    url(r'^$', 'index', name='distros_index'),
    url(r'^create/', 'create', name='create_distro'),
    url(r'^(?P<distro_id>[\d]+)/$', 'show', name='show_distro'),
    url(r'^(?P<distro_id>[\d]+)/update/$', 'update', name='update_distro'),
    url(r'^(?P<distro_id>[\d]+)/delete/$', 'delete', name='delete_distro'),
    )