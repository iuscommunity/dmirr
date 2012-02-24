
from cement2.core import controller
from dmirr.cli.controllers.base import dMirrResourceController
from dmirr.core import exc

class ProtocolController(dMirrResourceController):
    class Meta:
        label = 'protocols'
        description = 'dMirr Protocols Controller'
        arguments = [
            (['-l', '--label'], 
             dict(action='store', dest='label', metavar='STR',
                  help='protocol label (unique identifier)')),
            (['-p', '--port'], 
             dict(action='store', dest='port', metavar='STR',
                  help='protocol port')),
            (['resource'], 
             dict(action='store', nargs='?',
                  help='resource label to work with')), 
            (['-y', '--no-prompt'], 
             dict(dest='no_prompt', action='store_true', 
                  help='do not prompt for approval')),
            ]
        defaults = {}

    @controller.expose(help="create a new protocol resource")
    def create(self):
        self.validate_unique_resource(self.pargs.label)
        protocol = dict(label=self.pargs.label, port=self.pargs.port)
        response, data = self.hub.protocols.create(protocol)
        self.app.log.info("Protocol '%s' created." % protocol['label'])