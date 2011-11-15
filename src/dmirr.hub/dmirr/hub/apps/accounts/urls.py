
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('dmirr.hub.apps.accounts.views',
    url(r'^$', 'index_view'),
    #url(r'^post_social_redirect/', 'post_social_redirect_view'),
    #url(r'^social/', include('social_auth.urls')),    
    url(r'', include('userena.urls')),
)