
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from userena import views as userena_views

from dmirr.hub.apps.accounts.forms import dMirrSignupForm

urlpatterns = patterns('dmirr.hub.apps.accounts.views',
    #url(r'^$', 'index_view'),
    #url(r'^post_social_redirect/', 'post_social_redirect_view'),
    #url(r'^social/', include('social_auth.urls')),    
    url(r'^(?P<user>[\w\-\.\_]+)/groups/create/$', 'create_group', name='create_group'),
    url(r'^(?P<user>[\w\-\.\_]+)/groups/(?P<group>[\w\-\.\_]+)/update/$', 'update_group', name='update_group'),
    url(r'^(?P<user>[\w\-\.\_]+)/groups/(?P<group>[\w\-\.\_]+)/delete/$', 'delete_group', name='delete_group'),
    url(r'^(?P<user>[\w\-\.\_]+)/groups/(?P<group>[\w\-\.\_]+)/add/$', 'add_user_to_group', name='add_user_to_group'),
    url(r'^(?P<user>[\w\-\.\_]+)/groups/(?P<group>[\w\-\.\_]+)/remove/$', 'remove_user_from_group', name='remove_user_from_group'),
    url(r'^signup/$', userena_views.signup, name='userena_signup', 
                      kwargs=dict(signup_form=dMirrSignupForm)),
    url(r'', include('userena.urls')),
)