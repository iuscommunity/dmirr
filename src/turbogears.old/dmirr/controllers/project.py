# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
import re
from tg import expose, validate, flash, url, request, redirect, config, require
from repoze.what.predicates import Any, is_user, has_permission, not_anonymous, in_group
import transaction
from tg.exceptions import HTTPNotFound
import pylons
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

import pylons
from tg.controllers import RestController
from formencode import validators
from dmirr.model import DBSession, metadata, Project
from dmirr.model.product import ProductRelease
from dmirr.model.auth import User, Group
from dmirr.model.host import Host
from dmirr.model.sync_protocol import SyncProtocol
from dmirr.lib import helpers as _h
from dmirr.lib.exc import *



__all__ = ['ProjectController']


class ProjectController(RestController):
    @expose('dmirr.templates.%s.project.edit' % config['theme'])
    @validate(validators={
        "host_id": validators.Int(not_empty=True) })
    def assign_host(self, project_id, *a, **kw):
        errors = _h.get_validation_errors()
        p = DBSession.query(Project).filter_by(id=project_id).first()
        h = DBSession.query(Host).filter_by(id=kw.get('host_id', None)).first()
        
        _h.protect_obj(p)
        _h.protect_obj(h)

        if not p:
            raise HTTPNotFound
        if not h:
            raise HTTPNotFound    
        
        if errors:
            return dict(errors=errors, project=p)
            
        _p_label = p.label
        p.hosts.append(h)
        transaction.commit()
        redirect(url("/project/%s/edit#upstream_mirrors" % _p_label))
    
    
    @expose('dmirr.templates.%s.project.edit' % config['theme'])
    def unassign_host(self, project_id, host_id):
        p = DBSession.query(Project).filter_by(id=int(project_id)).first()
        h = DBSession.query(Host).filter_by(id=int(host_id)).first()
        
        _h.protect_obj(p)
        _h.protect_obj(h)

        if not p:
            raise HTTPNotFound
        if not h:
            raise HTTPNotFound    
                
        _p_label = p.label
        p.hosts.remove(h)
        transaction.commit()
        redirect(url("/project/%s/edit#upstream_mirrors" % _p_label))
        return dict(errors={}, project=p)    
    
        
    @expose('dmirr.templates.%s.project.get_one' % config['theme'])
    def get_one(self, label, *a, **kw):
        p = DBSession.query(Project).filter_by(label=label).first()
        site_hosts = []
        for s in p.sites:
            for h in s.hosts:
                h.sync_base_path = s.sync_base_path
                site_hosts.append(h)
        return dict(errors={}, project=p, site_hosts=site_hosts)


    @expose('dmirr.templates.%s.generic_get_all' % config['theme'])
    def get_all(self, *a, **kw):
        view = kw.get('view', None)
        if view and view == 'user':
            ps = DBSession.query(Project)\
                 .filter_by(user_id=request.identity['user'].user_id).all()
        else:         
            ps = DBSession.query(Project).all()
        return dict(page="project", errors={}, page_title="dMirr Projects",
                    projects=ps)
        
        
    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.project.new' % config['theme'])
    def new(self, *a, **kw):
        group = _h.get_group_by_name(kw.get('group_name', None))
        protocol = _h.get_protocol_by_name(kw.get('sync_protocol', None))
        if not protocol:
            protocol = DBSession.query(SyncProtocol).filter_by(label='rsync')\
                        .first()
        
        all_protocols = DBSession.query(SyncProtocol).all()
        
        p = Project()
        p.label = kw.get('label', None)
        p.display_name = kw.get('display_name', None)
        p.desc = kw.get('desc', None)
        p.url = kw.get('url', None)
        p.sync_base_path = kw.get('sync_base_path', None)
        p.sync_flags = kw.get('sync_flags', None)
        p.group = group
        p.sync_protocol = protocol
        transaction.doom()
        return dict(page='project', errors={}, project=p, 
                    all_protocols=all_protocols)

    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.project.edit' % config['theme'])
    def edit(self, project_label=None, *a, **kw):
        p = DBSession.query(Project).filter_by(label=project_label).first()
        
        all_protocols = DBSession.query(SyncProtocol).all()
        _h.protect_obj_modify(p)
        
        # only groups that both the logged in user, and the owner of the
        # project share.
        all_groups = []
        for group in request.identity['user'].groups:
            if p.user in group.users:
                all_groups.append(group)
        for group in p.user.groups:
            if request.identity['user'] in group.users:
                all_groups.append(group)
                
        all_hosts = []
        for host in request.identity['user'].hosts:
            if host.group in all_groups and not host in all_hosts:
                all_hosts.append(host)
            elif host.user == p.user:
                all_hosts.append(host)
        for group in all_groups:
            for host in group.hosts:
                if not host in all_hosts:
                    all_hosts.append(host)

        all_h = [x for x in all_hosts if x not in p.hosts]            
        return dict(page='project', errors={}, project=p, 
                    all_protocols=all_protocols, all_hosts=all_h)


    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.project.new' % config['theme'])
    @validate(validators={
        "label": validators.UnicodeString(not_empty=True),
        "display_name": validators.UnicodeString(not_empty=True),
        "desc": validators.String(not_empty=False),
        "sync_base_path": validators.UnicodeString(not_empty=True),
        "sync_protocol" : validators.UnicodeString(not_empty=True),
        "sync_flags" : validators.UnicodeString(not_empty=False),
        "url": validators.URL(not_empty=False) })
    def post(self, *a, **kw):
        errors = _h.get_validation_errors()
        group = _h.get_group_by_name(kw.get('group_name', None))
        protocol = _h.get_protocol_by_name(kw.get('sync_protocol', None))
        all_protocols = DBSession.query(SyncProtocol).all()
        
        if not group:
            errors['group'] = 'Group does not exist!'
        if not protocol:
            errors['sync_protocol'] = 'Sync Protocol does not exist!'
            
        p = Project()
        p.label = unicode(re.sub(' ', '_', kw['label']).lower())
        _label = p.label
        p.display_name = unicode(kw.get('display_name', None))
        p.desc = kw.get('desc', None)
        p.url = unicode(kw.get('url', None))
        p.user = request.identity['user']
        p.sync_base_path = unicode(kw.get('sync_base_path', None))
        p.sync_flags = unicode(kw.get('sync_flags', None))
        p.group = group
        p.sync_protocol = protocol
        
        if len(errors) > 0:
            transaction.doom()
            return dict(page="project", errors=errors, project=p,
                        all_protocols=all_protocols)
        DBSession.add(p)
        transaction.commit()
        flash(_("%s created successfully!" % kw['display_name']), 'info')
        redirect(url('/project/%s/edit' % _label))
        
        
    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.project.edit' % config['theme'])
    @validate(validators={
        "label": validators.UnicodeString(not_empty=True),
        "display_name": validators.UnicodeString(not_empty=True),
        "desc": validators.String(not_empty=False),
        "sync_base_path": validators.UnicodeString(not_empty=True),
        "sync_protocol" : validators.UnicodeString(not_empty=True),
        "sync_flags" : validators.UnicodeString(not_empty=False),
        "url": validators.URL(not_empty=False) })
    def put(self, project_id=None, *a, **kw):
        errors = _h.get_validation_errors()
        p = DBSession.query(Project).filter_by(id=project_id).first()
        if not p:
            raise HTTPNotFound
        if kw['label'] != p.label:
            other_p = DBSession.query(Project).filter_by(label=kw['label'])\
                      .first()
            if other_p:
                errors['label'] = "%s already exists, use another label." % \
                    other_p.label
        group = _h.get_group_by_name(kw.get('group_name', None))
        protocol = _h.get_protocol_by_name(kw.get('sync_protocol', None))
        all_protocols = DBSession.query(SyncProtocol).all()

        _h.protect_obj_modify(p)
        
        p.display_name = unicode(kw['display_name'])
        p.desc = kw['desc']
        p.url = unicode(kw['url'])
        p.sync_base_path = unicode(kw.get('sync_base_path', None))
        p.sync_flags = unicode(kw.get('sync_flags', None))
        p.sync_protocol = protocol
        p.group = group
        
        if len(errors) > 0:
            transaction.doom()
            return dict(errors=errors, project=p, all_protocols=all_protocols)

        p.label = unicode(re.sub(' ', '_', kw['label']).lower())
        _label = p.label
        transaction.commit()
        flash(_("%s updated successfully!" % kw['display_name']), 'info')
        redirect(url('/project/%s/edit' % _label))

        
    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.delete_wrapper' % config['theme'])
    def delete(self, project_label=None, *a, **kw):
        _p = DBSession.query(Project).filter_by(label=project_label).first()   
        if not _p:
            raise HTTPNotFound
        _p_label = _p.label
        _h.protect_obj(_p)
            
        confirmed = kw.get('confirmed', None)        
        if not confirmed:
            display_name = _p.display_name
            action = url('/project/%s/delete' % _p.label)
            came_from = url('/project/%s/edit' % _p_label)
            return dict(page="project", errors={}, display_name=display_name, action=action, came_from=came_from)
        else:
            DBSession.delete(_p)
            transaction.commit()
            flash(_("%s and all associated data have been deleted." % _p.display_name), 'info')
            redirect(url('/dashboard'))
