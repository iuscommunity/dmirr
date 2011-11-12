from cement2.core import controller
from dmirr.cli.controllers.base import dMirrBaseController
from dmirr.core import exc

class dMirrUserController(dMirrBaseController):
    class meta:
        interface = controller.IController
        label = 'user'
        description = 'dMirr User Resource Client Interface'
        arguments = []
        defaults = {}

    @controller.expose(help="register a new user account")
    def register(self):
        print('inside dmirr.cli.controllers.user.register')