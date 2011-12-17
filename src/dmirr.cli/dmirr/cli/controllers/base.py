
import drest
import httplib
from cement2.core import controller, hook
from dmirr.core import exc

BAD_RESPONSE_CODES = [
    401,
    403,
    404,
    500,
    ]
    
class dMirrResponseHandler(drest.response.ResponseHandler):
    def handle_response(self, response, content):
        if int(response['status']) in BAD_RESPONSE_CODES:
            raise exc.dMirrRequestError, "Received HTTP %s - %s" % \
                (response['status'], httplib.responses[int(response['status'])])
        return (response, content)
    
class dMirrBaseController(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'base'
        description = 'dMirr Command Line Interface'
        arguments = []
        defaults = dict(
            hub_api_baseurl='http://dmirr.example.com',
            hub_api_user='',
            hub_api_key='',
            )
        
    def __init__(self):
        super(dMirrBaseController, self).__init__()
        self.conn = None
        
    def setup(self, *args, **kw):
        super(dMirrBaseController, self).setup(*args, **kw)
        self.conn = drest.Connection(
            self.config.get('base', 'hub_api_baseurl'),
            response_handler=dMirrResponseHandler(),
            )
        self.conn.auth(
            dmirr_api_user=self.config.get('base', 'hub_api_user'),
            dmirr_api_key=self.config.get('base', 'hub_api_key'),    
            )
        
        # resources
        self.conn.add_resource('user')
        self.conn.add_resource('project', path='/projects')
        
    @controller.expose(hide=True)
    def default(self):
        raise exc.dMirrArgumentError('A sub-command is required.  See: --help')