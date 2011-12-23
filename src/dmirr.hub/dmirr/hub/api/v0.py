
from django.conf.urls.defaults import url

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.validation import FormValidation
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.api import Api
from tastypie.utils import trailing_slash

from dmirr.hub import db
from dmirr.hub.apps.projects.forms import ProjectForm
         
class dMirrAuthorization(DjangoAuthorization):
    def is_authorized(self, request, object=None):
        # user must be logged in to check permissions
        # authentication backend must set request.user
        if not hasattr(request, 'user'):
            return False
            
        # GET is always allowed
        if request.method == 'GET':
            return True
           
        # Some are ok to POST 
        ok_to_post = ['projects']
        
        if request.method == 'POST' and \
           self.resource_meta.resource_name in ok_to_post:
           return True
           
        # otherwise do more checks
        klass = self.resource_meta.object_class
        
        # cannot check permissions if we don't know the model
        if not klass or not getattr(klass, '_meta', None):
            return True
        
        permission_codes = {
            'POST': '%s.add_%s',
            'PUT': '%s.change_%s',
            'DELETE': '%s.delete_%s',
            }

        # cannot map request method to permission code name
        if request.method not in permission_codes:
            return True

        permission_code = permission_codes[request.method] % (
            klass._meta.app_label,
            klass._meta.module_name
            )

        # per obj permission check, if any fail return False
        for obj in self.resource_meta.queryset:
            res = request.user.has_perm(permission_code, obj)
            
            if not res:
                return False
                
        return True
        
    #def apply_limits(self, request, object_list):
    #    request.user.has_perm('projects.change_project')
    #    return object_list
        
class dMirrAuthentication(ApiKeyAuthentication):
    """
    Similar to APIKeyAuthentication, however uses dmirr_api_user and 
    dmirr_api_key as GET/POST params.
    
    """
    api_user_param = 'dmirr_api_user'
    api_key_param = 'dmirr_api_key'
    
    def __init__(self):
        super(dMirrAuthentication, self).__init__()

    def is_authenticated(self, request, **kwargs):
        """
        Finds the user and checks their API key.  Should return either 
        ``True`` if allowed, ``False`` if not.  Also returns true if 
        request.user.is_authenticated().
        
        """
        if request.user.is_authenticated():
            return True

        username = request.GET.get(self.api_user_param) or \
                   request.POST.get(self.api_user_param)
        api_key = request.GET.get(self.api_key_param) or \
                  request.POST.get(self.api_key_param)

        if not username or not api_key:
            return self._unauthorized()

        try:
            user = db.User.objects.get(username=username)
        except (db.User.DoesNotExist, db.User.MultipleObjectsReturned):
            return self._unauthorized()

        request.user = user
        res = self.get_key(user, api_key)
        
        # FIX ME > probably want to remove dmirr_api_user, dmirr_api_key from
        # the request object... but can't do that here cause request is 
        # immutable.

        return res
        
class dMirrResource(ModelResource):    
    pass

class UserResource(dMirrResource):    
    class Meta:
        queryset = db.User.objects.all()
        authentication = dMirrAuthentication()
        authorization = dMirrAuthorization()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {}
        allowed_methods = ['get', 'put']
        
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[a-zA-Z][\w\d_\.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
        
    def apply_authorization_limits(self, request, object_list):
        # just punt for now
        return object_list
    
        
class UserProfileResource(dMirrResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    
    class Meta:
        authentication = dMirrAuthentication()
        authorization = dMirrAuthorization()
        queryset = db.UserProfile.objects.all()
        resource_name = 'user_profile'
        excludes = []
        filtering = {}
        allowed_methods = ['get']
        
    def apply_authorization_limits(self, request, object_list):
        # just punt for now
        return object_list
        
class ProjectResource(dMirrResource):
    owner = fields.ToOneField(UserResource, 'user', full=True)
    
    class Meta:
        authentication = dMirrAuthentication()
        authorization = dMirrAuthorization()
        queryset = db.Project.objects.all()
        resource_name = 'projects'
        excludes = []
        filtering = {}
        allowed_methods = ['get', 'put', 'post']
        #dvalidation = FormValidation(form_class=ProjectForm)
        
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<label>[a-zA-Z][\w\d_\.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
        
v0_api = Api(api_name='v0')
v0_api.register(UserResource())
v0_api.register(UserProfileResource())
v0_api.register(ProjectResource())
