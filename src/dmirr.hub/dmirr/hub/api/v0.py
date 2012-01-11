
from django.conf.urls.defaults import url
from django.forms.models import ModelChoiceField

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
     

class dMirrValidation(FormValidation):
    """
    Override tastypie's standard ``FormValidation`` since this does not care
    about URI to PK conversion for ``ToOneField`` or ``ToManyField``.  Also
    properly handles unique fields on PUT.
    
    """

    def uri_to_pk(self, uri):
        """
        Returns the integer PK part of a URI.

        Assumes ``/api/v1/resource/123/`` format. If conversion fails, this just
        returns the URI unmodified.

        Also handles lists of URIs
        """

        if uri is None:
            return None

        # convert everything to lists
        multiple = not isinstance(uri, basestring)
        uris = uri if multiple else [uri]

        # handle all passed URIs
        converted = []
        for one_uri in uris:
            try:
                # hopefully /api/v1/<resource_name>/<pk>/
                converted.append(one_uri.split('/')[-2])
            except (IndexError, ValueError):
                raise ValueError(
                    "URI %s could not be converted to PK integer." % one_uri)

        # convert back to original format
        return converted if multiple else converted[0]

    def is_valid(self, bundle, request=None):
        data = bundle.data

        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}
            
        # copy data, so we don't modify the bundle
        data = data.copy()

        # convert URIs to PK integers for all relation fields
        relation_fields = [name for name, field in
                           self.form_class.base_fields.items()
                           if issubclass(field.__class__, ModelChoiceField)]

        for field in relation_fields:
            if field in data:
                data[field] = self.uri_to_pk(data[field])

        # validate and return messages on error
        if request.method == 'POST':    
            form = self.form_class(data)
        elif request.method == 'PUT':
            ### FIX ME: using resource_pk is a hack added in dehydrate()
            ### Look at: https://github.com/toastdriven/django-tastypie/issues/152
            obj = self.form_class.Meta.model.objects.get(pk=data['resource_pk'])
            form = self.form_class(data, instance=obj)
            
        if form.is_valid():
            return {}
            
        return form.errors
           

class dMirrAuthorization(DjangoAuthorization):
    def _user_has_perm(self, request, permission, obj):
        # user has permission on themself
        if request.user == obj:
            return True
            
        # user has permission if they own the object
        elif hasattr(obj, 'user') and request.user == obj.user:
            return True
        
        # otherwise user must actually have the permission per object
        elif request.user.has_perm(permission, obj):
            return True
            
        return False
        
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

        # need to ensure we have perms on related fields as well
        related_fields = [name for name, field in
                           self.resource_meta.validation.form_class.base_fields.items()
                           if issubclass(field.__class__, ModelChoiceField)]
                           

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
            # always check the object itself first
            if not self._user_has_perm(request, permission_code, obj):
                return False
            
            # then check any related fields
            for related_name in related_fields:
                related_obj = getattr(obj, related_name)
                if not self._user_has_perm(request, permission_code, related_obj):
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
    def dehydrate(self, bundle):
        bundle.data['resource_pk'] = bundle.obj.id
        return bundle

class UserResource(dMirrResource):    
    class Meta:
        queryset = db.User.objects.all()
        authentication = dMirrAuthentication()
        authorization = dMirrAuthorization()
        resource_name = 'users'
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
        resource_name = 'user_profiles'
        excludes = []
        filtering = {}
        allowed_methods = ['get']
        
    def apply_authorization_limits(self, request, object_list):
        # just punt for now
        return object_list
        
class ProjectResource(dMirrResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    
    class Meta:
        authentication = dMirrAuthentication()
        authorization = dMirrAuthorization()
        queryset = db.Project.objects.all()
        resource_name = 'projects'
        excludes = []
        filtering = {}
        allowed_methods = ['get', 'put', 'post', 'delete']
        validation = dMirrValidation(form_class=ProjectForm)
        
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<label>[a-zA-Z][\w\d_\.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
        
v0_api = Api(api_name='v0')
v0_api.register(UserResource())
v0_api.register(UserProfileResource())
v0_api.register(ProjectResource())
