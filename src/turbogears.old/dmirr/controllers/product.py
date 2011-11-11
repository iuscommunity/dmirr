# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
import re
from tg import expose, validate, flash, url, request, redirect, config, require
from tg.exceptions import HTTPNotFound
from repoze.what.predicates import Any, is_user, in_group, has_permission, not_anonymous
import transaction
import pylons
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import NotAuthorizedError
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

from tg.controllers import RestController
from dmirr.model import DBSession, metadata
from dmirr.model.auth import User, Group
from dmirr.model.project import Project
from dmirr.model.product import Product, ProductRelease, Arch
from dmirr.lib import helpers as _h
from dmirr.lib.exc import *
from formencode import validators


__all__ = ['ProductController', 'ProductReleaseController']


class ProductController(RestController):
    @expose('dmirr.templates.%s.product.get_one' % config['theme'])
    def get_one(self, project_label=None, *a, **kw):
        p = DBSession.query(Product).filter_by(label=project_label).first()
        return dict(page="product", errors={}, project=p.project, product=p)

    @expose('dmirr.templates.%s.product.get_all' % config['theme'])
    def get_all(self, *a, **kw):
        pass

    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.product.new' % config['theme'])
    def new(self, *a, **kw):
        project = DBSession.query(Project)\
                  .filter_by(label=kw.get('project', None)).first()
        if not project:
            raise HTTPNotFound, "Invalid Project"
            
        _h.protect_obj_modify(project)
        
        p = Product()
        p.label = kw.get('label', '')
        p.display_name = kw.get('display_name', '')
        p.desc = kw.get('desc', '')
        return dict(page='product', errors={}, project=project, product=p)

    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.product.edit' % config['theme'])    
    def edit(self, product_label=None, *a, **kw):
        product = _h.get_product_by_name(product_label)
        if not product:
            raise HTTPNotFound
        _h.protect_obj_modify(product.project)
            
        return dict(errors={}, project=product.project, product=product)

    
    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.product.new' % config['theme'])
    @validate(validators={
        "label": validators.UnicodeString(not_empty=True),
        "display_name": validators.UnicodeString(not_empty=True),
        "desc": validators.String(not_empty=False),
        "project_label": validators.UnicodeString(not_empty=True) })
    def post(self, *a, **kw):
        errors = _h.get_validation_errors()
        project = _h.get_project_by_name(kw.get('project_label', None))
        if not project:
            errors['project'] = "Project does not exist"
        
        _h.protect_obj_modify(project)
            
        _existing_p = _h.get_product_by_name(kw.get('label', None))
        if _existing_p:
            errors['label'] = "%s already exists!" % kw.get('label', None)
            
        p = Product()
        p.label = unicode(re.sub(' ', '_', kw['label']).lower())
        p.display_name = unicode(kw.get('display_name', None))
        p.desc = kw.get('desc', None)
        
        if len(errors) > 0:
            return dict(errors=errors, project=project, product=p)
            
        p.project = project
        
        DBSession.add(p)
        transaction.commit()
        flash(_("%s created successfully!" % kw['display_name']), 'info')
        redirect(url('/product/new?project=%s' % kw['project_label']))
        
        
    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.product.edit' % config['theme']) 
    @validate(validators={
        "label": validators.UnicodeString(not_empty=True),
        "display_name": validators.UnicodeString(not_empty=True),
        "desc": validators.String(not_empty=False),
        "project_label": validators.UnicodeString(not_empty=True) })
    def put(self, product_label=None, *a, **kw):
        p = DBSession.query(Product).filter_by(label=product_label).first()
        project = p.project
        _project_label = project.label    
        
        if not p:
            raise HTTPNotFound
        if not project:
            raise HTTPNotFound
        
        _h.protect_obj_modify(project)
        _h.protect_obj_modify(p.project)
        
        errors = _h.get_validation_errors()
        
        if kw.get('label', None) != p.label:
            _existing_p = _h.get_product_by_name(kw.get('label', None))
            if _existing_p:
                errors['label'] = "%s already exists!" % kw.get('label', None)
            
        p.label = unicode(re.sub(' ', '_', kw['label']).lower())
        p.display_name = unicode(kw['display_name'])
        p.desc = kw['desc']
        p.project = project
                    
        if errors:
            transaction.doom()
            return dict(project=p.project, errors=errors, product=p)

        transaction.commit()
        flash(_("%s updated successfully!" % kw['display_name']), 'info')
        redirect(url("/project/%s/edit#products" % _project_label))
        
        
    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.delete_wrapper' % config['theme'])
    def delete(self, product_label=None, *a, **kw):
        p = _h.get_product_by_name(product_label)
        _project_label = p.project.label
        if not p:
            raise HTTPNotFound
        
        _h.protect_obj_modify(p.project)
            
        confirmed = kw.get('confirmed', None)        
        if not confirmed:
            display_name = p.display_name
            action = url('/product/%s/delete' % p.label)
            came_from = url('/project/%s/edit' % _project_label)
            return dict(errors={}, display_name=display_name, 
                        action=action, came_from=came_from)
        else:
            DBSession.delete(p)
            transaction.commit()
            flash(_("%s and all associated data have been deleted." % \
                p.display_name), 'info')
            redirect(url('/project/%s/edit' % _project_label))


class ProductReleaseController(RestController):
    @expose('dmirr.templates.%s.product_release.get_one' % config['theme'])
    def get_one(self, release_label=None, *a, **kw):
        r = _h.get_release_by_name(release_label)
        return dict(errors={}, release=r)


    @expose('dmirr.templates.%s.product_release.get_all' % config['theme'])
    def get_all(self, *a, **kw):
        pass


    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.product_release.new' % config['theme'])
    def new(self, *a, **kw):
        product = _h.get_product_by_name(kw.get('product', None))
        all_archs = DBSession.query(Arch).all()
        if not product:
            raise HTTPNotFound
            
        _h.protect_obj_modify(product.project)
        
        r = ProductRelease()
        r.label = kw.get('label', '')
        r.display_name = kw.get('display_name', '')
        r.desc = kw.get('desc', '')
        arch = DBSession.query(Arch)\
            .filter_by(label=kw.get('arch_label', 'noarch'))\
            .first()
        r.path = kw.get('path', '')
        return dict(page='product_release', errors={}, project=product.project, product=product, all_archs=all_archs, arch=arch, release=r)


    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.product_release.edit' % config['theme'])    
    def edit(self, release_label=None, *a, **kw):
        r = _h.get_release_by_name(release_label)
        all_archs = DBSession.query(Arch).all()
        if not r:
            raise HTTPNotFound
        
        _h.protect_obj_modify(r.product.project)            
        return dict(project=r.product.project, errors={}, all_archs=all_archs, 
                    release=r)
    
    
    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.product_release.new' % config['theme'])
    @validate(validators={
        "label": validators.UnicodeString(not_empty=True),
        "display_name": validators.UnicodeString(not_empty=True),
        "archs": validators.UnicodeString(not_empty=True),
        "desc": validators.String(not_empty=False),
        "path": validators.UnicodeString(not_empty=True),
        "product_label": validators.UnicodeString(not_empty=True) })
    def post(self, *a, **kw):
        errors = _h.get_validation_errors()
        product = _h.get_product_by_name(kw.get('product_label', None))
        allarchs = DBSession.query(Arch).all()
        if not product:
            raise HTTPNotFound
        _product_label = product.label
        
        _h.protect_obj_modify(product.project)
        
        r = ProductRelease()
        
        _existing_r = _h.get_release_by_name(kw.get('label', None))
        if _existing_r:
            errors['label'] = "%s already exists!" % kw.get('label', None)
        
        if len(errors) > 0:
            transaction.doom()
            return dict(errors=errors, project=product.project, 
                        all_archs=allarchs, product=product, release=r)
        
        r.product = product
        r.label = unicode(re.sub(' ', '_', kw['label']).lower())
        r.display_name = unicode(kw.get('display_name', None))
        r.desc = kw.get('desc', None)
        r.path = unicode(kw.get('path', ''))
            
        if not kw.get('archs'):
            errors['archs'] = "Must select atleast one arch"
        else:
            for a in allarchs:
                if _(a.id) in kw['archs']:
                    r.archs.append(a)
                else:
                    if a in r.archs:
                        r.archs.remove(a)
                        
        # FIX ME: Add check to make sure the rsync path is valid
        
        DBSession.add(r)
        transaction.commit()
        flash(_("%s created successfully!" % kw['display_name']), 'info')
        redirect(url('/product_release/new?product=%s' % _product_label))
        
        
    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.product_release.edit' % config['theme'])
    @validate(validators={
        "label": validators.UnicodeString(not_empty=True),
        "display_name": validators.UnicodeString(not_empty=True),
        "archs": validators.UnicodeString(not_empty=True),
        "desc": validators.String(not_empty=False),
        "path": validators.UnicodeString(not_empty=True),
        "product_label": validators.UnicodeString(not_empty=True) })
    def put(self, release_id=None, *a, **kw):
        errors = _h.get_validation_errors()
        r = DBSession.query(ProductRelease)\
            .filter_by(id=release_id)\
            .first()
        product = r.product
        allarchs = DBSession.query(Arch).all()
        _project_label = r.product.project.label
        
        if not r:
            raise HTTPNotFound
        
        _h.protect_obj_modify(r.product.project)
        _h.protect_obj_modify(product.project)
            
        r.label = unicode(re.sub(' ', '_', kw['label']).lower())
        r.display_name = unicode(kw.get('display_name', None))
        r.desc = kw.get('desc', None)
        r.path = unicode(kw.get('path', ''))
        r.product = product
        
        if kw.get('label') != r.label:
            existing_r = _h.get_release_by_name(kw.get('label', None))
            if _existing_r:
                errors['label'] = "%s already exists!" % kw.get('label', None)
    
        if not kw.get('archs'):
            errors['archs'] = "Must select atleast one arch"
        else:
            for a in allarchs:
                if _(a.id) in kw['archs']:
                    r.archs.append(a)
                else:
                    if a in r.archs:
                        r.archs.remove(a)
                
        if len(errors) > 0:
            transaction.doom()
            return dict(errors=errors, project=r.product.project, 
                        all_archs=allarchs, release=r)

        transaction.commit()
        flash(_("%s updated successfully!" % kw['display_name']), 'info')
        redirect(url('/project/%s/edit#products' % _project_label))


    @require(has_permission('dmirr_project'))
    @expose('dmirr.templates.%s.delete_wrapper' % config['theme'])
    def delete(self, release_label=None, *a, **kw):
        r = DBSession.query(ProductRelease)\
            .filter_by(label=release_label)\
            .first()
        _project_label = r.product.project.label
        if not r:
            raise HTTPNotFound
            
        _h.protect_obj_modify(r.product.project)
            
        confirmed = kw.get('confirmed', None)
        display_name = r.display_name
        action = url('/product_release/%s/delete' % r.label)
        came_from = url('/project/%s/edit' % _project_label)
        if not confirmed:
            return dict(page="product_release", errors={}, display_name=display_name, action=action, came_from=came_from)
        else:
            DBSession.delete(r)
            transaction.commit()
            flash(_("%s and all associated data have been deleted." % display_name), 'info')
            redirect(url('/project/%s/edit' % _project_label))
