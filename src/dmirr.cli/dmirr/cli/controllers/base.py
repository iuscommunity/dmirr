
import drest
import httplib
from pkg_resources import get_distribution
from cement2.core import controller, hook
from dmirr.core import exc
    
VERSION = get_distribution('dmirr.cli').version
CEMENT_VERSION = get_distribution('cement2').version
BANNER = """
dMirr Command Line Interface v%s, Built on Cement v%s
Copyright (c) 2009,2012 Rackspace US, Inc.
Distributed under the GNU GPL v2 License

[[[[[[[]]]]]]] [[[[[[[]]]]]]]
[[[[[[[]]]]]]]       [[[[[[[]]]]]]]
[[[[[[[]]]]]]] [[[[[[[]]]]]]]
[[[[[[[]]]]]]] [[[[[[[]]]]]]]


http://github.com/rackspace/dmirr
""" % (VERSION, CEMENT_VERSION)
    
class dMirrRequestHandler(drest.request.TastyPieRequestHandler):
    def handle_response(self, response, content):
        if (400 <= int(response.status) <=499) or (response.status == 500):
            msg = "Received HTTP Code %s - %s" % (
                   response.status, 
                   httplib.responses[int(response.status)])
            if int(response.status) == 400:
                raise exc.dMirrAPIError(msg, errors=content)

            raise drest.exc.dRestRequestError(
                msg, response=response, content=content
                )
            
        return (response, content)
        
class dMirrAPI(drest.api.TastyPieAPI):
    class Meta:
        request = dMirrRequestHandler
        
def paginate(prefix, line_length, text):
    line = ''
    new_text = ''
    for word in text.split():
        if len(line) + len(word) > int(line_length):
            new_text = "%s %s %s\n%s" % (new_text, line, word, prefix)
            line = ''
        else:
            if line == '':
                line = word
            else:
                line = "%s %s" % (line, word)        
    return new_text.strip()

class dMirrAbstractBaseController(controller.CementBaseController):
    def __init__(self):
        super(dMirrAbstractBaseController, self).__init__()
        self.hub = None
        
    def _setup(self, *args, **kw):
        super(dMirrAbstractBaseController, self)._setup(*args, **kw)
        self.hub = dMirrAPI(
            self.config.get('base', 'hub_api_baseurl')
            )
        self.hub.auth(
            user=self.config.get('base', 'hub_api_user'),
            api_key=self.config.get('base', 'hub_api_key'),    
            )

        # this is only useful in resource controllers
        self.resource = getattr(self.hub, self._meta.label, None)
              
class dMirrBaseController(dMirrAbstractBaseController):
    class Meta:
        label = 'base'
        description = 'dMirr Command Line Interface'
        arguments = [
            (['--version'], dict(action='version', version=BANNER)),
            ]
        defaults = dict(
            hub_api_baseurl='http://dmirr.example.com',
            hub_api_user='',
            hub_api_key='',
            )
    
    @controller.expose(help="show the api users info")
    def whoami(self):
        response, user = self.hub.users.get(self.config.get('base', 'hub_api_user'))
        print self.render(user, 'users/show.txt')
        
    @controller.expose(hide=True)
    def default(self):
        if not self.app.argv or self.app.argv[0].startswith('-'):
            raise exc.dMirrArgumentError(
                "A sub-command is required.  " + \
                "Try: 'dmirr %s --help'." % self._meta.label)
        else:
            raise exc.dMirrArgumentError(
                "Unknown sub-command '%s'.  " % self.app.argv[0] + \
                "Try: 'dmirr %s --help'." % self._meta.label)
    
class dMirrResourceController(dMirrAbstractBaseController):
    """
    This is a special controller to be subclassed from for any resource 
    controllers.  It uses self._meta.label as the resource, thereby eliminating
    a lot of redundant code.
    
    """
    def __init__(self):
        super(dMirrResourceController, self).__init__()

    def validate_unique_resource(self, label):
        try:
            assert label, "Label required (-l, --label)."
        except AssertionError, e:
            raise exc.dMirrArgumentError, e.args[0]
            
        try:
            response, project = self.resource.get(label)
            if not response.status == 410:
                raise exc.dMirrArgumentError(
                    "The resource '%s/%s/' already exists." % \
                        (self._meta.label, label)
                    )
        except drest.exc.dRestRequestError as e:
            if int(e.response.status) == 404:
                return True
            else:
                raise

        return True

    @controller.expose(help="list all resources")
    def listall(self):
        """
        Listall using self._meta.label as the resource.
        """
        response, data = self.resource.get()
        for obj in data['objects']:
            if self._meta.label == 'users':
                print obj['username']
            else:
                print obj['label']
        
    @controller.expose(help="show all resource data")
    def show(self):
        try:
            assert self.pargs.resource, "Resource argument required."
        except AssertionError, e:
            raise exc.dMirrArgumentError, e.args[0]
            
        response, data = self.resource.get(self.pargs.resource)

        if 'description' in data:
            data['description'] = paginate('%16s' % ' ', 50, data['description'])
            
        data['response'] = response
        print self.render(data, '%s/show.txt' % self._meta.label)

    @controller.expose(help="delete an existing resource")    
    def delete(self):
        response, data = self.resource.get(self.pargs.resource)
        if self.pargs.no_prompt:
            res = 'yes'
        else:
            msg = "Really delete '%s' and all associated data? [y/N] " % \
                   self.pargs.resource
            res = raw_input(msg).strip()
                       
        try:
            assert self.pargs.resource, "Resource argument required."
        except AssertionError, e:
            raise exc.dMirrArgumentError, e.args[0]

        if res.lower() in ['yes', 'y', '1']:
            self.resource.delete(self.pargs.resource)
            self.log.info("Permanently deleted '%s'" % self.pargs.resource)

    @controller.expose(help="create a new resource", hide=True)
    def create(self):
        self.validate_unique_resource(self.pargs.label)
        
        data = dict()
        for key in self.resource.schema['fields']:
            if key == 'user':
                if not self.pargs.user:
                    self.pargs.user = self.config.get('base', 'hub_api_user')
                response, user = self.hub.users.get(self.pargs.user)
                self.pargs.user = user['resource_uri']
                
            if hasattr(self.pargs, key) and getattr(self.pargs, key, None):
                data[key] = getattr(self.pargs, key)

        self.resource.create(data)
        self.log.info("Created '%s'." % self.pargs.label)
        
    @controller.expose(help="update an existing resource")
    def update(self):
        try:
            assert self.pargs.resource, "Resource argument required."
        except AssertionError, e:
            raise exc.dMirrArgumentError, e.args[0]
            
        response, data = self.resource.get(self.pargs.resource)
        _data = data.copy()
        for key in _data:
            if hasattr(self.pargs, key) and getattr(self.pargs, key, None):
                data[key] = getattr(self.pargs, key)
                    
        self.resource.update(data['id'], data)
        self.app.log.info("Updated '%s'." % data['label'])
    