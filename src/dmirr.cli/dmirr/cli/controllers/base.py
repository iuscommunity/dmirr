
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
    
class dMirrBaseController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
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
        
    def __init__(self):
        super(dMirrBaseController, self).__init__()
        self.hub = None
        
    def _setup(self, *args, **kw):
        super(dMirrBaseController, self)._setup(*args, **kw)
        self.hub = drest.api.TastyPieAPI(
            self.config.get('base', 'hub_api_baseurl')
            )
        self.hub.auth(
            user=self.config.get('base', 'hub_api_user'),
            api_key=self.config.get('base', 'hub_api_key'),    
            )

        # this is only useful in resource controllers
        self.resource = getattr(self.hub, self._meta.label, None)
        
    @controller.expose(hide=True)
    def default(self):
        raise exc.dMirrArgumentError('A sub-command is required.  See: --help')
    
class dMirrResourceController(dMirrBaseController):
    """
    This is a special controller to be subclassed from for any resource 
    controllers.  It uses self._meta.label as the resource, thereby eliminating
    a lot of redundant code.
    
    """
    def __init__(self):
        super(dMirrResourceController, self).__init__()
    
    def validate_unique_resource(self, label):
        try:
            assert label, "%s label required." % self._meta.label.capitalize()
        except AssertionError, e:
            raise exc.dMirrArgumentError, e.args[0]
            
        try:
            response, project = self.resource.get(label)
            if not response.status == 410:
                raise exc.dMirrArgumentError(
                    "The %s '%s' already exists." % (self.resource, label)
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
            assert self.pargs.resource, \
                "%s label required." % self._meta.label.capitalize()
        except AssertionError, e:
            raise exc.dMirrArgumentError, e.args[0]
            
        response, data = self.resource.get(self.pargs.resource)

        print self.render(data, '%s/show.txt' % self._meta.label)

    @controller.expose(help="delete an existing resource")    
    def delete(self):
        res = raw_input("Are you sure you want to delete the %s %s: [y/N] " % \
                       (self._meta.label, self.pargs.resource)).strip()
                       
        try:
            assert self.pargs.resource, \
                "%s label required." % self._meta.label.capitalize()
        except AssertionError, e:
            raise exc.dMirrArgumentError, e.args[0]

        if res.lower() in ['yes', 'y', '1']:
            self.resource.delete(self.pargs.resource)
            self.log.info("Deleted the %s %s" % \
                         (self._meta.label, self.pargs.resource))
