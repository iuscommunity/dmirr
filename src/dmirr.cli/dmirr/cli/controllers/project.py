from cement2.core import controller
from dmirr.cli.controllers.base import dMirrBaseController
from dmirr.core import exc

class ProjectController(dMirrBaseController):
    class meta:
        interface = controller.IController
        label = 'project'
        description = 'dMirr Project Resource Client Interface'
        arguments = []
        defaults = {}

    @controller.expose(help="create a new project")
    def create(self):
        response, project = self.conn.project.get(1)
        self.conn.project.update(project)
        
        
    