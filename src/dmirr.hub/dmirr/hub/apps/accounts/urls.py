
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from userena import views as userena_views

from dmirr.hub.apps.accounts.forms import dMirrSignupForm

urlpatterns = patterns('dmirr.hub.apps.accounts.views',
    #url(r'^$', 'index_view'),
    #url(r'^post_social_redirect/', 'post_social_redirect_view'),
    #url(r'^social/', include('social_auth.urls')),    
    
    ### API KEY
    url(r'^(?P<user>[\w\-\.\_]+)/api_access/$', 'show_api_key', name='show_api_key'),
    url(r'^(?P<user>[\w\-\.\_]+)/reset_api_key/$', 'reset_api_key', name='reset_api_key'),
    
    url(r'^(?P<user>[\w\-\.\_]+)/projects/$', 
        direct_to_template, dict(template='accounts/projects.html'),
        name='my_projects'),
    url(r'^(?P<user>[\w\-\.\_]+)/groups/$', 
        direct_to_template, dict(template='accounts/groups.html'), 
        name='my_groups'),
    url(r'^(?P<user>[\w\-\.\_]+)/systems/$', 
        direct_to_template, dict(template='accounts/systems.html'), 
        name='my_systems'),
    
    url(r'^groups/$', 
        'groups_index', 
        name='groups_index'),
    url(r'^groups/create/$', 
        'create_group', 
        name='create_group'),
    url(r'^groups/(?P<group>[\d]+)/$', 
        'show_group', 
        name='show_group'),
    url(r'^groups/(?P<group>[\d]+)/update/$', 
        'update_group', 
        name='update_group'),
    url(r'^groups/(?P<group>[\d]+)/delete/$', 
        'delete_group', 
        name='delete_group'),
    url(r'^groups/(?P<group>[\d]+)/add/$', 
        'add_user_to_group', 
        name='add_user_to_group'),
    url(r'^groups/(?P<group>[\d]+)/remove/$', 
        'remove_user_from_group', 
        name='remove_user_from_group'),
    url(r'^signup/$', 
        userena_views.signup, name='userena_signup', 
        kwargs=dict(signup_form=dMirrSignupForm)),
        
    url(r'', include('userena.urls')),
)