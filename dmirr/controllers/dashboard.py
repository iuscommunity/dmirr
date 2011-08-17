# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, validate, flash, url, request, redirect, config, require
from repoze.what.predicates import Any, is_user, has_permission, not_anonymous
import transaction
import pylons
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

from dmirr.lib.base import BaseController
from dmirr.model import DBSession, metadata
from dmirr.lib import helpers as _h
from dmirr.lib.exc import *
from formencode import validators


__all__ = ['DashboardController']


class DashboardController(BaseController):
    @expose('dmirr.templates.%s.dashboard.index' % config['theme'])
    def index(self, *a, **kw):
        all_projects = []
        for project in request.identity['user'].projects:
            if not project in all_projects:
                all_projects.append(project)
        for group in request.identity['user'].groups:
            for project in group.projects:
                if not project in all_projects:
                    all_projects.append(project)
        
        all_sites = []
        for site in request.identity['user'].sites:
            if not site in all_sites:
                all_sites.append(site)
        for group in request.identity['user'].groups:
            for site in group.sites:
                if not site in all_sites:
                    all_sites.append(site)
                    
        all_hosts = []
        for host in request.identity['user'].hosts:
            if not host in all_hosts:
                all_hosts.append(host)
        for group in request.identity['user'].groups:
            for host in group.hosts:
                if not host in all_hosts:
                    all_hosts.append(host)
                    
        if request.identity:
            return dict(page='dashboard', errors={}, all_projects=all_projects,
                        all_sites=all_sites, all_hosts=all_hosts)
        else:
            redirect(url('/'))
