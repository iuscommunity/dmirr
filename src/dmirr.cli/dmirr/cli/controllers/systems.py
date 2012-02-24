
from cement2.core import controller
from dmirr.cli.controllers.base import dMirrResourceController
from dmirr.core import exc

class SystemController(dMirrResourceController):
    class Meta:
        label = 'systems'
        description = 'dMirr Systems Controller'
        arguments = [
            (['resource'], 
             dict(action='store', nargs='?',
                  help='resource label to work with')), 
            ]
        defaults = {}
