# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect, config, \
               tmpl_context
               
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what import predicates

from dmirr.lib import helpers as _h
from dmirr.lib.base import BaseController
from dmirr.model import DBSession, metadata
from dmirr.controllers.error import ErrorController
from dmirr import model
from dmirr.controllers.secure import SecureController
from dmirr.controllers.project import ProjectController
from dmirr.controllers.product import ProductController, ProductReleaseController
from dmirr.controllers.site import SiteController
from dmirr.controllers.host import HostController
from dmirr.controllers.dashboard import DashboardController
from dmirr.controllers.mirrorlist import MirrorListController
from dmirr.controllers.user import UserController
from dmirr.controllers.group import GroupController
from dmirr.widgets.user_form import create_user_form

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the dmirr application.
    
    All the other controllers and WSGI applications should be mounted on this
    controller. For example::
    
        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()
    
    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.
    
    """

    #admin = Catwalk(model, DBSession)
    
    error = ErrorController()
    project = ProjectController()
    product = ProductController()
    product_release = ProductReleaseController()
    site = SiteController()
    host = HostController()
    user = UserController()
    group = GroupController()
    index = project
    dashboard = DashboardController()
    mirrorlist = MirrorListController()
    
    #@expose('dmirr.templates.%s.index' % config['theme'])
    #def index(self):
    #    """Handle the front-page."""
    #    return dict(page='index')

    @expose('dmirr.templates.%s.about'% config['theme'])
    def about(self):
        version = _h.get_version()
        return dict(page='about', errors={}, version=version)

    @expose('dmirr.templates.%s.login' % config['theme'])
    def login(self, came_from=url('/')):
        """Start the user login."""
        if config['user_registration'] == 'closed':
            flash(_('User registration is currently closed'), 'warning')
            
        errors = _h.get_validation_errors()
        tmpl_context.form = create_user_form
        terms_of_use=open(config['terms_of_use_file']).read()

        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='user', login_counter=str(login_counter),
                    page_title='New User Registration', came_from=came_from,
                    errors=errors, terms_of_use=terms_of_use)
    
    @expose()
    def post_login(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.
        
        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect(url('/login', came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.
        
        """
        flash(_('We hope to see you soon!'))
        redirect('/')
