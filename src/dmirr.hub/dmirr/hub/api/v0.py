
from django.conf.urls.defaults import url
from django.forms.models import ModelChoiceField

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.validation import FormValidation
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.api import Api
from tastypie.utils import trailing_slash
from tastypie.exceptions import ImmediateHttpResponse

from dmirr.hub import db
from dmirr.hub.apps.projects.forms import ProjectForm
from dmirr.hub.apps.archs.forms import ArchForm
from dmirr.hub.apps.protocols.forms import ProtocolForm
from dmirr.hub.apps.systems.forms import SystemForm, SystemResourceForm
    

def check_perm(request, perm, obj=None, raise_on_fail=True):
    fail = False
    
    if obj:
        if not request.user.has_perm(perm, obj):
            fail = True
    else:
        if not request.user.has_perm(perm):
            fail = True
        
    if fail and raise_on_fail:
        raise ImmediateHttpResponse(response=HttpUnauthorized())
    elif fail:
        return False
    else:
        return True

"""
def check_user_is_admin(request, obj, raise_on_fail=False):
    if request.user == obj.user:
        return True
    elif hasattr(obj, 'admin_group') and obj.admin_group:
        if request.user in obj.admin_group.user_set():
            return True

    if raise_on_fail:
        raise ImmediateHttpResponse(response=HttpUnauthorized())
    else:
        return False
    
def check_admin_group(request, obj, raise_on_fail=True):
    if not hasattr(obj, 'admin_group'):
        return True
    elif not obj.admin_group:
        return True
    elif obj.admin_group not in request.user.groups.all():
        if raise_on_fail:
            raise ImmediateHttpResponse(response=HttpUnauthorized())
        else:
            return False
""" 
                     
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
                if type(data[field]) == dict:
                    data[field] = self.uri_to_pk(data[field]['resource_uri'])
                else:
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
           

class dMirrAuthorization(Authorization):
    def __init__(self):
        super(dMirrAuthorization, self).__init__()
        
class dMirrAuthentication(ApiKeyAuthentication):
    def __init__(self):
        super(dMirrAuthentication, self).__init__()
        
    def is_authenticated(self, request, **kwargs):
        if request.user.is_authenticated():
            return True

        return super(dMirrAuthentication, self).is_authenticated(request, **kwargs)

class dMirrMeta:
    authentication = dMirrAuthentication()
    authorization = dMirrAuthorization()
    allowed_methods = ['get', 'put', 'post', 'delete']
    filtering = {}
    
class dMirrResource(ModelResource):    
    def dehydrate(self, bundle):
        bundle.data['resource_pk'] = bundle.obj.id
        return bundle
                                        
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % \
               (self._meta.resource_name, trailing_slash()), 
                self.wrap_view('dispatch_list'), 
                name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema%s$" % \
                (self._meta.resource_name, trailing_slash()), 
                self.wrap_view('get_schema'), 
                name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/set/(?P<pk_list>\w[\w/;-]*)/$" \
                % self._meta.resource_name, 
                self.wrap_view('get_multiple'), 
                name="api_get_multiple"),
            url(r"^(?P<resource_name>%s)/(?P<label>[a-zA-Z][\w\d_\.-]+)/$" % \
                self._meta.resource_name, 
                self.wrap_view('dispatch_detail'), 
                name="api_dispatch_detail"),
        ]
        
class UserResource(dMirrResource):    
    profile = fields.ToOneField('dmirr.hub.api.v0.UserProfileResource', 
                                'profile', full=True)
    
    class Meta(dMirrMeta):
        queryset = db.User.objects.all()
        resource_name = 'users'
        allowed_methods = ['get']
        excludes = [
            'password', 
            'is_active', 
            'is_staff', 
            'is_superuser',
            ]
        
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % \
               (self._meta.resource_name, trailing_slash()), 
                self.wrap_view('dispatch_list'), 
                name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema%s$" % \
               (self._meta.resource_name, trailing_slash()), 
                self.wrap_view('get_schema'), 
                name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/set/(?P<pk_list>\w[\w/;-]*)/$" % \
                self._meta.resource_name, 
                self.wrap_view('get_multiple'), 
                name="api_get_multiple"),
            url(r"^(?P<resource_name>%s)/(?P<username>[a-zA-Z][\w\d\_\.\-]+)/$" % \
                self._meta.resource_name, 
                self.wrap_view('dispatch_detail'), 
                name="api_dispatch_detail"),
        ]
        
    def dehydrate_email(self, bundle):
        if bundle.request.user.is_superuser:
            return bundle.obj.email
        else:
            return '************'
         
class UserProfileResource(dMirrResource):
    class Meta(dMirrMeta):
        queryset = db.UserProfile.objects.all()
        resource_name = 'user_profiles'
        allowed_methods = ['get']
        
    def dehydrate(self, bundle):
        if bundle.obj.user.profile.privacy == 'closed' \
           and not bundle.request.user.is_superuser:
           for key in bundle.data:
               if key.startswith('resource_'):
                   continue
               bundle.data[key] = '************'
        return bundle
        
class ProjectResource(dMirrResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    
    class Meta(dMirrMeta):
        queryset = db.Project.objects.all()
        resource_name = 'projects'
        validation = dMirrValidation(form_class=ProjectForm)
        
class ArchResource(dMirrResource):
    class Meta(dMirrMeta):
        queryset = db.Arch.objects.all()
        resource_name = 'archs'
        validation = dMirrValidation(form_class=ArchForm)
        
class ProtocolResource(dMirrResource):
    class Meta(dMirrMeta):
        queryset = db.Protocol.objects.all()
        resource_name = 'protocols'
        validation = dMirrValidation(form_class=ProtocolForm)


class SystemResource(dMirrResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    
    class Meta(dMirrMeta):
        queryset = db.System.objects.all()
        resource_name = 'systems'
        validation = dMirrValidation(form_class=SystemForm)
"""
    def _hide_data(self, bundle, field):
        res = check_perm(bundle.request, 
                         self._meta.change_perm, 
                         bundle.obj, 
                         False)
        if not res:
            return '************'
        else:
            return field
            
    def dehydrate_contact_name(self, bundle):
        return self._hide_data(bundle, bundle.obj.contact_name)

    def dehydrate_contact_email(self, bundle):
        return self._hide_data(bundle, bundle.obj.contact_email)
"""
class SystemResourceResource(dMirrResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    system = fields.ToOneField(SystemResource, 'system', full=True)
    project = fields.ToOneField(ProjectResource, 'project', full=True)
    protocols = fields.ToManyField(ProtocolResource, 'protocols', full=True)

    class Meta(dMirrMeta):
        queryset = db.SystemResource.objects.all()
        resource_name = 'systemresource'
        validation = dMirrValidation(form_class=SystemResourceForm)
     
v0_api = Api(api_name='v0')
v0_api.register(UserResource())
v0_api.register(UserProfileResource())
v0_api.register(ProjectResource())
v0_api.register(ArchResource())
v0_api.register(ProtocolResource())
v0_api.register(SystemResource())
v0_api.register(SystemResourceResource())
