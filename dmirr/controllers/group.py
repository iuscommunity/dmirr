# -*- coding: utf-8 -*-
"""group controller with all its actions protected."""
import re
from tg import expose, validate, flash, url, request, redirect, config, \
               require, tmpl_context

from repoze.what.predicates import Any, has_permission, not_anonymous
import transaction
import pylons
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission
from formencode import validators
from tg.exceptions import HTTPNotFound
from tg.controllers import RestController
import turbomail

from dmirr import model as model
from dmirr.model import DBSession as db
from dmirr.lib import helpers as _h
from dmirr.lib.exc import *
from dmirr.widgets.group_form import *



__all__ = ['GroupController']

class GroupController(RestController):  
    @expose('json')
    @expose('dmirr.templates.%s.generic_new_form' % config['theme'])
    def process_new_form_errors(self, *args, **kw):
        if pylons.request.response_type == 'application/json':
            kw['errors'] = pylons.tmpl_context.form_errors
            return dict(kw)
        else:
            errors = _h.get_validation_errors()
            tmpl_context.form = create_group_form
            return dict(page='group', page_title='New Group Registration', 
                        errors=errors)
    
    @expose('json')
    @require(has_permission('dmirr_group'))
    @expose('dmirr.templates.%s.generic_edit_form' % config['theme'])
    def process_edit_form_errors(self, *args, **kw):
        if pylons.request.response_type == 'application/json':
            kw['errors'] = pylons.tmpl_context.form_errors
            return dict(kw)
        else:
            group = db.query(model.Group)\
                    .filter_by(group_id=kw.get('group_id', None)).first()
            _h.protect_group_obj(group)
            
            tmpl_context.form = edit_group_form
            tmpl_context.form2 = add_to_group_form
            return dict(page='group', page_title='Edit Account Settings', 
                        group=group)
                  
    @expose('json')                
    @require(has_permission('dmirr_group'))
    @expose('dmirr.templates.%s.generic_edit_form' % config['theme'])
    @validate(add_to_group_form, error_handler=process_edit_form_errors)
    def assign_user(self, *a, **kw):  
        g = db.query(model.Group).filter_by(group_id=kw['group_id']).first()
        u = db.query(model.User).filter_by(user_name=kw['user_name']).first()
        _g_label = g.group_name
        _h.protect_group_obj(g)
        _h.protect_user_obj(u)

        if not g:
            raise HTTPNotFound
        if not u:
            raise HTTPNotFound    
                
        g.users.append(u)
        transaction.commit()
        redirect(url("/group/%s/edit" % _g_label))
    
    @require(has_permission('dmirr_group'))
    @expose('dmirr.templates.%s.generic_edit_form' % config['theme'])
    def unassign_user(self, group_id, user_id):
        g = db.query(model.Group).filter_by(group_id=group_id).first()
        u = db.query(model.User).filter_by(user_id=user_id).first()
        _g_label = g.group_name
        _h.protect_group_obj(g)
        _h.protect_user_obj(u)
            
        if not g:
            raise HTTPNotFound
        if not u:
            raise HTTPNotFound    
        
        if g.owner.user_id == u.user_id:
                flash(_('Can not remove the group owner.'), 'warning')
                redirect(url("/group/%s/edit" % _g_label))
                
        g.users.remove(u)
        transaction.commit()
        redirect(url("/group/%s" % _g_label))
                  
    @expose('json')
    @expose('dmirr.templates.%s.group.get_one' % config['theme'])
    def get_one(self, group_name=None, *a, **kw):
        g = db.query(model.Group).filter_by(group_name=group_name).first()
        return dict(page='group', errors={}, group=g)
        
    @expose('json')
    @expose('dmirr.templates.%s.generic_get_all' % config['theme'])
    def get_all(self, *a, **kw):
        groups = db.query(model.Group).all()
        return dict(errors={}, page='group', page_title="dMirr Groups",
                    groups=groups)
        
    @require(has_permission('dmirr_group'))    
    @expose('dmirr.templates.%s.generic_new_form' % config['theme'])
    def new(self, *a, **kw):
        errors = _h.get_validation_errors()
        tmpl_context.form = create_group_form
        return dict(page='group', page_title='New Group Registration', 
                    errors=errors)

    @require(has_permission('dmirr_group'))
    @expose('dmirr.templates.%s.generic_edit_form' % config['theme'])
    def edit(self, group_name=None, **kw):
        group = db.query(model.Group).filter_by(group_name=group_name).first()
        if not group:
            raise HTTPNotFound
        
        _h.protect_group_obj(group)
            
        errors = _h.get_validation_errors()
        tmpl_context.form = edit_group_form
        tmpl_context.form2 = add_to_group_form
        return dict(page='group', page_title='Edit Group Settings', 
                    errors=errors, group=group)
                            
    @expose('json')
    @require(has_permission('dmirr_group'))
    @validate(create_group_form, error_handler=process_new_form_errors)
    def post(self, **kw):
        errors = _h.get_validation_errors()
                      
        g = model.Group()
        g.group_name = unicode(re.sub(' ', '_', kw['group_name']).lower())
        g.display_name = unicode(kw['display_name'])
        g.owner = request.identity['user']
        g.users.append(g.owner)     

        db.add(g)
        transaction.commit()
        flash(_('%s group has been registered.' % kw['display_name']), 'info')
        redirect(url('/dashboard'))

    @expose('json')
    @require(has_permission('dmirr_group'))
    @validate(edit_group_form, error_handler=edit)
    def put(self, *a, **kw):
        u = db.query(model.Group).filter_by(group_id=kw.get('group_id', None))\
            .first()
        if not u:
            raise HTTPNotFound
                            
        _h.protect_group_obj(u)
        
        u.display_name = unicode(kw['display_name'])
        
        transaction.commit()
        flash(_("%s group settings have been saved." % kw['display_name']), 'info')
        redirect(url('/dashboard'))
        
    @require(has_permission('dmirr_group'))
    @expose('dmirr.templates.%s.delete_wrapper' % config['theme'])
    def delete(self, group_name=None, *a, **kw):
        g = db.query(model.Group).filter_by(group_name=group_name).first()
        _display_name = g.display_name
        if not g:
            raise HTTPNotFound
        
        _h.protect_group_obj(g)
        
        came_from = url('/group/%s/edit' % g.group_name)
        
        if g.group_name == 'dmirr_admin':
            flash(_("Can not delete %s." % g.display_name), 'warning')
            redirect(came_from)
        
        if g.group_name == 'dmirr_everyone':
            flash(_("Can not delete %s group." % g.display_name), 'warning')
            redirect(came_from)
                
        confirmed = kw.get('confirmed', None)        
        if not confirmed:
            display_name = g.display_name
            action = url('/group/%s/delete' % g.group_name)
            return dict(errors={}, display_name=display_name, action=action, 
                        came_from=came_from)
        else:
            db.delete(g)
            transaction.commit()
            flash(_("The %s group and all associated data have been deleted." % \
                    _display_name), 'info')
            redirect(url('/dashboard'))
