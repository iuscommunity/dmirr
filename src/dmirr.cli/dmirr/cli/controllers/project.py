
import sys
from cement2.core import controller
from dmirr.cli.controllers.base import dMirrResourceController
from dmirr.core import exc

class ProjectController(dMirrResourceController):
    class Meta:
        interface = controller.IController
        label = 'project'
        description = 'dMirr Project Resource Client Interface'
        arguments = [
            (['-l', '--label'], 
             dict(action='store', dest='label', metavar='STR',
                  help='project label (unique identifier)')),
            (['--display-name'], 
             dict(action='store', dest='display_name', metavar='TEXT',
                  help='project display name')),
            (['-d', '--description'], 
             dict(action='store', dest='description', metavar='STR',
                  help='project description')),
            (['--private'], 
             dict(action='store', dest='private', metavar='STR',
                  help='privitization flag (boolean)')),
            (['-u', '--user'], 
             dict(action='store', dest='user', metavar='STR',
                  help='user label (username)')),
            (['--url'], 
             dict(action='store', dest='url', metavar='URL',
                  help='full URL path')),
            (['resource'], 
             dict(action='store', nargs='?',
                  help='resource label to work with')), 
            ]
        defaults = {}

    
    @controller.expose(help="create a new project")
    def create(self):
        self.validate_unique_resource(self.pargs.label)
            
        if not self.pargs.user:
            self.pargs.user = self.config.get('base', 'hub_api_user')
        
        response, user = self.hub.user.get(self.pargs.user)

        try:
            assert self.pargs.label, "Project label required."
        except AssertionError, e:
            raise exc.dMirrArgumentError, e.args[0]
            
        response, user = self.hub.user.get(self.pargs.user)
        
        project = dict(
            label=self.pargs.label,
            display_name=self.pargs.display_name,
            description=self.pargs.description,
            private=self.pargs.private,
            user=user['resource_uri'],
            )
        
        response, data = self.hub.project.create(params=project)
        if int(response['status']) != 201:
            print data['error_message']

        self.app.log.info("Project %s created." % self.pargs.label)
        
    @controller.expose(help="update an existing project resource")
    def update(self):
        try:
            assert self.pargs.resource, "Project resource argument required."
        except AssertionError, e:
            raise exc.dMirrArgumentError, e.args[0]
            
        response, project = self.hub.project.get(self.pargs.resource)
        project = project.copy()
        for key in project:
            if hasattr(self.pargs, key) and getattr(self.pargs, key, None):
                if key == 'user':
                    _, user = self.hub.user.get(pargs.user)
                    project['user'] = user
                else:
                    project[key] = getattr(self.pargs, key)
        
        # fix things up
        project['user'] = project['user']['resource_uri']
        self.hub.project.update(project['id'], project)
      
    