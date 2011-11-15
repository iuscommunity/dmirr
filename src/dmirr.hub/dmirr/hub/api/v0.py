
from django.conf.urls.defaults import url

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.api import Api
from tastypie.utils import trailing_slash

from dmirr.hub import db
 
class ApiKeyPlusWebAuthentication(ApiKeyAuthentication):
    def is_authenticated(self, request, **kwargs):
        if request.user.is_authenticated():
            return True

        return super(ApiKeyPlusWebAuthentication, self).is_authenticated(request, **kwargs)

    def get_identifier(self, request):
        if request.user.is_authenticated():
            return request.user.username
        else:
            return super(ApiKeyPlusWebAuthentication, self).get_identifier(request)
            
class UserResource(ModelResource):    
    class Meta:
        queryset = db.User.objects.all()
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DjangoAuthorization()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {}
        allowed_methods = ['get']
        
    #def override_urls(self):
    #    return [
    #        url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
    #    ]
        
class UserProfileResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    
    class Meta:
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DjangoAuthorization()
        queryset = db.UserProfile.objects.all()
        resource_name = 'user_profile'
        excludes = []
        filtering = {}
        allowed_methods = ['get']
        
        
v0_api = Api(api_name='v0')
v0_api.register(UserResource())
v0_api.register(UserProfileResource())
