
from django.conf.urls.defaults import patterns, include, url
from dmirr.hub.api.v0 import v0_api

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'dmirr.hub.apps.base.views.index_view'),
    url(r'^account/', include('dmirr.hub.apps.accounts.urls')),
    url(r'^archs/', include('dmirr.hub.apps.archs.urls')),
    url(r'^projects/', include('dmirr.hub.apps.projects.urls')),
    url(r'^api/', include(v0_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('dmirr.hub.apps.repos.urls')),
)
