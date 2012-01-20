
from django.conf.urls.defaults import patterns, include, url
from dmirr.hub.api.v0 import v0_api

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'dmirr.hub.apps.base.views.index_view'),
    url(r'^account/', include('dmirr.hub.apps.accounts.urls')),
    url(r'^archs/', include('dmirr.hub.apps.archs.urls')),
    url(r'^protocols/', include('dmirr.hub.apps.protocols.urls')),
    url(r'^projects/', include('dmirr.hub.apps.projects.urls')),
    url(r'^systems/', include('dmirr.hub.apps.systems.urls')),
    url(r'^api/', include(v0_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('dmirr.hub.apps.repos.urls')),
    url(r'^(?P<project>[\w\-\.\_]+)/$', 'dmirr.hub.apps.projects.views.show', name='show_project'),
    url(r'^(?P<project>[\w\-\.\_]+)/update/$', 'dmirr.hub.apps.projects.views.update', name='update_project'),
    url(r'^(?P<project>[\w\-\.\_]+)/delete/$', 'dmirr.hub.apps.projects.views.delete', name='delete_project'),
)
