
from cement2.core import controller
from dmirr.cli.controllers.base import dMirrResourceController
from dmirr.core import exc

class ProtocolController(dMirrResourceController):
    class Meta:
        label = 'protocols'
        description = 'dMirr Protocols Controller'
        arguments = [
            (['resource'], 
             dict(action='store', nargs='?',
                  help='resource label to work with')), 
            ]
        defaults = {}
