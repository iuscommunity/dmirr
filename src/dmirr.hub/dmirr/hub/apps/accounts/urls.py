
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from userena import views as userena_views

from dmirr.hub.apps.accounts.forms import dMirrSignupForm

urlpatterns = patterns('dmirr.hub.apps.accounts.views',
    #url(r'^$', 'index_view'),
    #url(r'^post_social_redirect/', 'post_social_redirect_view'),
    #url(r'^social/', include('social_auth.urls')),    
    url(r'^signup/$', userena_views.signup, name='userena_signup', 
                      kwargs=dict(signup_form=dMirrSignupForm)),
    url(r'', include('userena.urls')),
)

