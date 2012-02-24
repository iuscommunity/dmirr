
from cement2.core import controller
from dmirr.cli.controllers.base import dMirrResourceController
from dmirr.core import exc

class SystemController(dMirrResourceController):
    class Meta:
        label = 'systems'
        description = 'dMirr Systems Controller'
        arguments = [
            (['-l', '--label'], 
             dict(action='store', dest='label', metavar='STR',
                  help='system label (unique identifier)')),
            (['--contact-name'], 
             dict(action='store', dest='contact_name', metavar='STR',
                  help='system contact name')),
            (['--contact-email'], 
             dict(action='store', dest='contact_email', metavar='STR',
                  help='system contact email address')),
            (['resource'], 
             dict(action='store', nargs='?',
                  help='system resource label to work with')), 
            (['-y', '--no-prompt'], 
             dict(dest='no_prompt', action='store_true', 
                  help='do not prompt for approval')),
            (['-u', '--user'], 
             dict(action='store', dest='user', metavar='STR',
                  help='user label (username)')),
            ]
        defaults = {}

    