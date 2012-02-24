
from cement2.core import controller
from dmirr.cli.controllers.base import dMirrResourceController
from dmirr.core import exc

class ArchController(dMirrResourceController):
    class Meta:
        label = 'archs'
        description = 'dMirr Archs Controller'
        arguments = [
            (['-l', '--label'], 
             dict(action='store', dest='label', metavar='STR',
                  help='project label (unique identifier)')),
            (['resource'], 
             dict(action='store', nargs='?',
                  help='resource label to work with')), 
            (['-y', '--no-prompt'], 
             dict(dest='no_prompt', action='store_true', 
                  help='do not prompt for approval')),
            ]
        defaults = {}

    @controller.expose(help="create a new arch")
    def create(self):
        self.validate_unique_resource(self.pargs.label)
        arch = dict(label=self.pargs.label)
        response, data = self.hub.archs.create(arch)
        self.app.log.info("Arch '%s' created." % arch['label'])
        
    @controller.expose(help="update an existing arch resource")
    def update(self):
        try:
            assert self.pargs.resource, "Arch resource argument required."
        except AssertionError, e:
            raise exc.dMirrArgumentError, e.args[0]
            
        response, arch = self.hub.archs.get(self.pargs.resource)
        _arch = arch.copy()
        for key in _arch:
            if hasattr(self.pargs, key) and getattr(self.pargs, key, None):
                arch[key] = getattr(self.pargs, key)
                    
        self.hub.archs.update(arch['id'], arch)
        self.app.log.info("Arch '%s' update." % arch['label'])
    