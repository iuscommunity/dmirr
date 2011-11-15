
from django.conf.urls.defaults import patterns, include, url
from dmirr.hub.api.v0 import v0_api

urlpatterns = patterns('',
    url(r'^$', 'dmirr.hub.apps.base.views.index_view'),
    url(r'^account/', include('dmirr.hub.apps.accounts.urls')),
    url(r'^api/', include(v0_api.urls)),
)
