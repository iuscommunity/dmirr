from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dmirr.hub.apps.mirrorlist.views',
    url(r'^$', 'mirrorlist', name='mirrorlist'),
    )