from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'dmirr.hub.apps.base.views.index_view'),
    url(r'^account/', include('dmirr.hub.apps.accounts.urls')),
)
