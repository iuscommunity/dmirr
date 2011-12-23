
import drest
import httplib
from pkg_resources import get_distribution
from cement2.core import controller, hook
from dmirr.core import exc
    
class dMirrRequestHandler(drest.RequestHandler):
    def request(self, *args, **kw):
        try:
            return super(dMirrRequestHandler, self).request(*args, **kw)
        except drest.exc.dRestRequestError as e:
            raise exc.dMirrRequestError(e.msg)
        
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
        
    def setup(self, *args, **kw):
        super(dMirrBaseController, self).setup(*args, **kw)
        self.hub = drest.Connection(
            self.config.get('base', 'hub_api_baseurl'),
            request_handler=dMirrRequestHandler(),
            )
        self.hub.auth(
            dmirr_api_user=self.config.get('base', 'hub_api_user'),
            dmirr_api_key=self.config.get('base', 'hub_api_key'),    
            )
        
        # resources
        self.hub.add_resource('user')
        self.hub.add_resource('project', path='/projects')
        
    @controller.expose(hide=True)
    def default(self):
        raise exc.dMirrArgumentError('A sub-command is required.  See: --help')
    
    def validate_unique_resource(self, resource, label):
        try:
            res_obj = getattr(self.hub, resource)
            response, project = res_obj.get(label)
            if not response.status == 410:
                raise exc.dMirrArgumentError(
                    "The %s '%s' already exists." % (resource, label)
                    )
        except exc.dMirrRequestError as e:
            pass

        return True