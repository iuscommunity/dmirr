
from cement2.core import handler
from dmirr.cli.controllers.base import dMirrBaseController
from dmirr.cli.controllers.user import UserController
from dmirr.cli.controllers.project import ProjectController

handler.register(dMirrBaseController)
handler.register(UserController)
handler.register(ProjectController)
