# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
import re
from tg import expose, validate, flash, url, request, redirect, config, require
from tg.exceptions import HTTPNotFound
from repoze.what.predicates import Any, is_user, has_permission, not_anonymous
import transaction
import pylons
from pylons.i18n import ugettext as _, lazy_ugettext as l_

from tg.controllers import RestController
from dmirr.model import DBSession, metadata
from dmirr.model.auth import User, Group
from dmirr.model.site import Site
from dmirr.model.host import Host
from dmirr.model.project import Project, SiteSyncPath
from dmirr.lib import helpers as _h
from dmirr.lib.exc import *

from formencode import validators



__all__ = ['SiteController']

            
class SiteController(RestController):
    def _add_site_sync_path(self, site_id, project_id, sync_path):
        s = DBSession.query(Site).filter_by(id=site_id).first()
        p = DBSession.query(Project).filter_by(id=project_id).first()
        alt = DBSession.query(SiteSyncPath).filter_by(site_id=s.id)\
              .filter_by(project_id=p.id).first()
        if alt:
            alt.sync_path = sync_path
            transaction.commit()
            return alt
    
        alt = SiteSyncPath()
        alt.site = s
        alt.project = p
        alt.sync_path = sync_path
        DBSession.add(alt)
        transaction.commit()
        return alt
    
    @require(has_permission('dmirr_site'))
    @expose('dmirr.templates.%s.site.edit' % config['theme'])
    @validate(validators={
        "host_id": validators.Int(not_empty=True) })
    def assign_host(self, site_id, *a, **kw):
        errors = _h.get_validation_errors()
        s = DBSession.query(Site).filter_by(id=site_id).first()
        h = DBSession.query(Host).filter_by(id=kw.get('host_id', None)).first()
        
        _h.protect_obj(s)
        _h.protect_obj(h)

        if not s:
            raise HTTPNotFound
        if not h:
            raise HTTPNotFound    
        
        if errors:
            return dict(errors=errors, site=s)
            
        _s_label = s.label
        s.hosts.append(h)
        transaction.commit()
        redirect(url("/site/%s/edit#downstream_mirrors" % _s_label))
    
    @require(has_permission('dmirr_site'))
    @expose('dmirr.templates.%s.site.edit' % config['theme'])
    def unassign_host(self, site_id, host_id):
        s = DBSession.query(Site).filter_by(id=int(site_id)).first()
        h = DBSession.query(Host).filter_by(id=int(host_id)).first()
        
        _h.protect_obj(s)
        _h.protect_obj(h)

        if not s:
            raise HTTPNotFound
        if not h:
            raise HTTPNotFound    
                
        _s_label = s.label
        s.hosts.remove(h)
        transaction.commit()
        redirect(url("/site/%s/edit#downstream_mirrors" % _s_label))
        return dict(errors={}, site=s)    
    
    @require(has_permission('dmirr_site'))
    @expose('dmirr.templates.%s.site.edit' % config['theme'])
    @validate(validators={
        "project_id": validators.Int(not_empty=True) })
    def assign_project(self, site_id, *a, **kw):
        errors = _h.get_validation_errors()
        s = DBSession.query(Site).filter_by(id=site_id).first()
        p = DBSession.query(Project).filter_by(id=kw.get('project_id', None))\
            .first()
        all_p = DBSession.query(Project).all()
        
        _h.protect_obj(s)
        _h.protect_obj(p)

        if not s:
            raise HTTPNotFound
        if not p:
            raise HTTPNotFound    
        
        all_projects = [x for x in all_p if x not in s.projects]
        
        if errors:
            transaction.doom()
            return dict(errors=errors, site=s, all_projects=all_projects)

        _s_label = s.label
        s.projects.append(p)

        if kw.get('sync_path', None):
            self._add_site_sync_path(s.id, p.id, kw['sync_path'])
        else:
            transaction.doom()
            flash(_('Site sync path required for each project.'), 'warning')
            redirect(url("/site/%s/edit#mirrored_projects" % _s_label))

        transaction.commit()    
        redirect(url("/site/%s/edit#projects" % _s_label))
    
    @require(has_permission('dmirr_site'))
    @expose('dmirr.templates.%s.site.edit' % config['theme'])
    def unassign_project(self, site_id, project_id):
        s = DBSession.query(Site).filter_by(id=int(site_id)).first()
        p = DBSession.query(Project).filter_by(id=int(project_id)).first()
        
        _h.protect_obj(s)
        _h.protect_obj(p)

        if not s:
            raise HTTPNotFound
        if not p:
            raise HTTPNotFound    
                
        _s_label = s.label
        
        sync_path = DBSession.query(SiteSyncPath).filter_by(site_id=s.id)\
              .filter_by(project_id=p.id).first()
        if sync_path:
            DBSession.delete(sync_path)
            
        s.projects.remove(p)
        transaction.commit()
        
        redirect(url("/site/%s/edit#mirrored_projects" % _s_label))
    
    
    @expose('dmirr.templates.%s.site.get_one' % config['theme'])
    def get_one(self, site_label=None, *a, **kw):
        s = _h.get_site_by_name(site_label)
        _h.protect_obj(s)
        return dict(page='site', errors={}, site=s)
        
        
    @expose('dmirr.templates.%s.site.get_all' % config['theme'])
    def get_all(self, *a, **kw):
        pass
        
        
    @require(has_permission('dmirr_site'))
    @expose('dmirr.templates.%s.site.new' % config['theme'])
    def new(self, *a, **kw):
        group = _h.get_group_by_name(kw.get('group_name', None))
        s = Site()
        s.label = kw.get('label', None)
        s.display_name = kw.get('display_name', None)
        s.desc = kw.get('desc', None)
        s.url = kw.get('url', None)
        s.contact_name = kw.get('contact_name', None)
        s.contact_email = kw.get('contact_email', None)
        s.sync_base_path = kw.get('sync_base_path', None)
        s.user = request.identity['user']
        s.group = group
        
        transaction.doom()
        return dict(page='site', errors={}, site=s)


    @require(has_permission('dmirr_site'))
    @expose('dmirr.templates.%s.site.edit' % config['theme'])
    def edit(self, site_label=None, *a, **kw):
        s = _h.get_site_by_name(site_label)
        all_projects = DBSession.query(Project).all()

        # only groups that both the logged in user, and the owner of the
        # site share.
        all_groups = []
        for group in request.identity['user'].groups:
            if s.user in group.users:
                all_groups.append(group)
        for group in s.user.groups:
            if request.identity['user'] in group.users:
                all_groups.append(group)
                
        all_hosts = []
        for host in request.identity['user'].hosts:
            if host.group in all_groups and not host in all_hosts:
                all_hosts.append(host)
            elif host.user == s.user:
                all_hosts.append(host)
        for group in all_groups:
            for host in group.hosts:
                if not host in all_hosts:
                    all_hosts.append(host)
                    
        
        if not s:
            raise HTTPNotFound
            
        _h.protect_obj_modify(s)
        
        # I love python...
        all_p = [x for x in all_projects if x not in s.projects]
        all_h = [x for x in all_hosts if x not in s.hosts]
        return dict(errors={}, site=s, all_projects=all_p, all_hosts=all_h)


    @require(has_permission('dmirr_site'))
    @expose('dmirr.templates.%s.site.new' % config['theme'])
    @validate(validators={
        "label": validators.UnicodeString(not_empty=True),
        "display_name": validators.UnicodeString(not_empty=True),
        "desc": validators.String(not_empty=False),
        "contact_name": validators.UnicodeString(not_empty=False),
        "contact_email" : validators.Email(resolve_domain=False),
        "sync_base_path" : validators.UnicodeString(not_empty=True),
        "url": validators.URL(not_empty=False) })
    def post(self, *a, **kw):
        errors = _h.get_validation_errors()
        group = _h.get_group_by_name(kw.get('group_name', None))
        all_p = DBSession.query(Project).all()
        if not group:
            errors['group'] = 'Group does not exist!'
            
        s = Site()
        s.label = unicode(re.sub(' ', '_', kw['label']).lower())
        s.display_name = unicode(kw.get('display_name', None))
        s.desc = kw.get('desc', None)
        s.url = unicode(kw.get('url', None))
        s.contact_name = unicode(kw.get('contact_name', None))
        s.contact_email = unicode(kw.get('contact_email', None))
        s.sync_base_path = unicode(kw.get('sync_base_path', None))
        s.user = request.identity['user']
        s.group = group
    
        if len(errors) > 0:
            all_projects = [x for x in all_p if x not in s.projects]
            all_hosts = [x for x in request.identity['user'].hosts \
                            if x not in s.hosts]
            transaction.doom()
            return dict(page='site', errors=errors, site=s, 
                        all_projects=all_projects, all_hosts=all_hosts)
            
        DBSession.add(s)
        transaction.commit()
        flash(_("%s created successfully!" % kw['display_name']), 'info')
        redirect(url('/dashboard'))


    @require(has_permission('dmirr_site'))
    @expose('dmirr.templates.%s.site.edit' % config['theme'])
    @validate(validators={
        "label": validators.UnicodeString(not_empty=True),
        "display_name": validators.UnicodeString(not_empty=True),
        "desc": validators.String(not_empty=False),
        "contact_name": validators.UnicodeString(not_empty=False),
        "contact_email" : validators.Email(resolve_domain=False),
        "sync_base_path" : validators.UnicodeString(not_empty=True),
        "url": validators.URL(not_empty=True) })
    def put(self, site_label=None, *a, **kw):
        errors = _h.get_validation_errors()
        s = DBSession.query(Site).filter_by(label=site_label).first()
        group = _h.get_group_by_name(kw.get('group_name', None))
        all_p = DBSession.query(Project).all()
        _h.protect_obj(s)
        
        if not s:
            raise HTTPNotFound         
        if not group:
            errors['group'] = 'Group does not exist!'
            
        s.label = unicode(re.sub(' ', '_', kw['label']).lower())
        s.display_name = unicode(kw.get('display_name', None))
        s.desc = kw.get('desc', None)
        s.url = unicode(kw.get('url', None))
        s.contact_name = unicode(kw.get('contact_name', None))
        s.contact_email = unicode(kw.get('contact_email', None))
        s.sync_base_path = unicode(kw.get('sync_base_path', None))
        s.user = request.identity['user']
        s.group = group
    
        if len(errors) > 0:
            all_projects = [x for x in all_p if x not in s.projects]
            all_hosts = [x for x in request.identity['user'].hosts \
                            if x not in s.hosts]
            transaction.doom()
            return dict(page='site', errors=errors, site=s,
                        all_projects=all_projects, all_hosts=all_hosts)
            
        transaction.commit()
        flash(_("%s updated successfully!" % kw['display_name']), 'info')
        redirect(url('/site/%s/edit' % kw['label']))
        

    @require(has_permission('dmirr_site'))
    @expose('dmirr.templates.%s.delete_wrapper' % config['theme'])
    def delete(self, site_label=None, *a, **kw):
        s = DBSession.query(Site).filter_by(label=site_label).first()
        _display_name = s.display_name
        if not s:
            raise HTTPNotFound
        
        _h.protect_obj(s)
        
        confirmed = kw.get('confirmed', None)        
        if not confirmed:
            display_name = s.display_name
            action = url('/site/%s/delete' % s.label)
            came_from = url('/site/%s/edit' % s.label)
            return dict(errors={}, display_name=display_name, action=action, 
                        came_from=came_from)
        else:
            DBSession.delete(s)
            transaction.commit()
            flash(_("%s and all associated data have been deleted." % \
                    _display_name), 'info')
            redirect(url('/dashboard'))
            
            
