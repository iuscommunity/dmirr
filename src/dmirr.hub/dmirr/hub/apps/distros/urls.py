
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dmirr.hub.apps.distros.views',
    url(r'^(?P<project>[\w]+)/distros/$', 'index', name='distros_index'),
    url(r'^(?P<project>[\w]+)/distros/create/$', 'create', name='create_distro'),
    url(r'^(?P<project>[\w]+)/distros/(?P<distro>[\w]+)/$', 'show', name='show_distro'),
    url(r'^(?P<project>[\w]+)/distros/(?P<distro>[\w]+)/update/$', 'update', name='update_distro'),
    url(r'^(?P<project>[\w]+)/distros/(?P<distro>[\w]+)/delete/$', 'delete', name='delete_distro'),
    )