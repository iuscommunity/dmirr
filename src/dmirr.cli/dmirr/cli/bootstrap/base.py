
from cement2.core import handler
from dmirr.cli.controllers.base import dMirrBaseController
from dmirr.cli.controllers.users import UserController
from dmirr.cli.controllers.projects import ProjectController
from dmirr.cli.controllers.archs import ArchController
from dmirr.cli.controllers.protocols import ProtocolController
from dmirr.cli.controllers.systems import SystemController

handler.register(dMirrBaseController)
handler.register(UserController)
handler.register(ProjectController)
handler.register(ArchController)
handler.register(ProtocolController)
handler.register(SystemController)