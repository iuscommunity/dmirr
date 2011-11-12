
from cement2.core import controller
from dmirr.core import exc

class dMirrBaseController(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'base'
        description = 'dMirr Command Line Interface'
        arguments = []
        defaults = {}
        
    def __init__(self):
        super(dMirrBaseController, self).__init__()
    
    @controller.expose(hide=True)
    def default(self):
        raise exc.dMirrArgumentError('A sub-command is required.  See: --help')