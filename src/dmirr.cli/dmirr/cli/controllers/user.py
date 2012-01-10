from cement2.core import controller
from dmirr.cli.controllers.base import dMirrResourceController
from dmirr.core import exc

class UserController(dMirrResourceController):
    class Meta:
        interface = controller.IController
        label = 'user'
        description = 'dMirr User Resource Client Interface'
        arguments = [
            (['resource'], 
             dict(action='store', nargs='?',
                  help='resource label to work with')), 
            ]
        defaults = {}
