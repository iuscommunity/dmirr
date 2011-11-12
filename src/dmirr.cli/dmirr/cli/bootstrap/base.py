
from cement2.core import handler
from dmirr.cli.controllers.base import dMirrBaseController
from dmirr.cli.controllers.user import dMirrUserController

handler.register(dMirrBaseController)
handler.register(dMirrUserController)