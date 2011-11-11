# -*- coding: utf-8 -*-
"""host controller with all its actions protected."""
from tg import expose, validate, flash, url, request, redirect, config, require
from repoze.what.predicates import Any, is_user, has_permission, not_anonymous
import transaction
from tg.exceptions import HTTPNotFound
from repoze.what.predicates import NotAuthorizedError
import pylons
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission
import pygeoip
from pygeoip import GeoIPError
from socket import gaierror
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

from tg.controllers import RestController
from dmirr.model import DBSession, metadata
from dmirr.model.auth import User, Group
from dmirr.model.site import Site
from dmirr.model.status import Status
from dmirr.model.host import Host
from dmirr.model.project import Project
from dmirr.lib import helpers as _h
from dmirr.lib.exc import *
from formencode import validators


__all__ = ['HostController']


class HostController(RestController):
    @expose('dmirr.templates.%s.host.get_one' % config['theme'])
    def get_one(self, address=None):    
        h = DBSession.query(Host).filter_by(address=address).first()
        return dict(errors={}, host=h)
     
     
    def _get_geoip_data(self, host):
        gic = pygeoip.GeoIP(config['geo_city_file'])
        try:
            res = gic.record_by_name(host)
        except gaierror, e:
            res = None
        return res
     
                
    @expose('dmirr.templates.%s.about' % config['theme'])
    def get_all(self, *a, **kw):
        pass
        
        
    @require(has_permission('dmirr_host'))
    @expose('dmirr.templates.%s.host.new' % config['theme'])
    def new(self, *a, **kw):
        h = Host()
        group   = _h.get_group_by_name(kw.get('group_name', None))
        project = _h.get_project_by_name(kw.get('project_label', None))
        site    = _h.get_site_by_name(kw.get('site_label', None))
            
        _h.protect_obj(project)
        _h.protect_obj(site)
        
        h.user = request.identity['user']
        h.address = kw.get('address', 'host.example.com').strip()
        h.group = group
        transaction.doom()
        return dict(errors={}, host=h)
        
        
    @require(has_permission('dmirr_host'))
    @expose('dmirr.templates.%s.host.edit' % config['theme'])
    def edit(self, host_address=None, *a, **kw):
        h = _h.get_host_by_address(host_address)
        if not h:
            raise HTTPNotFound
            
        _h.protect_obj(h)
        return dict(errors={}, original_host=h, host=h)
                    
                    
    @require(has_permission('dmirr_host'))
    @expose('dmirr.templates.%s.host.new' % config['theme'])
    @validate(validators={
        "address": validators.UnicodeString(not_empty=True),
        "group_name": validators.UnicodeString(not_empty=True)})
    def post(self, *a, **kw):
        h = _h.get_host_by_address(kw.get('address', None))
        errors  = _h.get_validation_errors()
        if h:
            errors['address'] = "Host %s already exists!" % h.address

        h = Host()            
        group = _h.get_group_by_name(kw.get('group_name', None))
        
        h.address = unicode(kw['address'].strip())
        h.user = request.identity['user']
        h.group = group
        
        res = self._get_geoip_data(h.address)
        if not res:
            errors['host_address'] = "The host '%s' could " % h.address + \
                                     "not be identified via GeoIP. " + \
                                     "Please ensure the hostname resolves" 
                    
        if errors:
            transaction.doom()
            return dict(errors=errors, host=h)
        
        _h.protect_obj(h)
        h.online_status = DBSession.query(Status)\
                          .filter_by(label='Offline').first()
        h.city = unicode(res.get('city', None))
        h.region_name   = unicode(res.get('region_name', None))
        h.longitude     = res.get('longitude', None)
        h.latitude      = res.get('latitude', None)
        h.country_name  = unicode(res.get('country_name', None))
        h.country_code  = unicode(res.get('country_code', None))
        h.country_code3 = unicode(res.get('country_code3', None))
        h.postal_code   = res.get('postal_code', None)
            
        flash(_("%s created successfully!" % kw['address']), 'info')
        redirect(url('/host/new'))
        

    @require(has_permission('dmirr_host'))
    @expose('dmirr.templates.%s.host.edit' % config['theme'])
    @validate(validators={
        "address": validators.UnicodeString(not_empty=True),
        "group_name": validators.UnicodeString(not_empty=True)})
    def put(self, host_id=None, *a, **kw):
        h = DBSession.query(Host).filter_by(id=host_id).first()
        if not h:
            raise HTTPNotFound
            
        errors  = _h.get_validation_errors()
        h.user  = request.identity['user']
        h.group = _h.get_group_by_name(kw.get('group_name', None))
        h.address = unicode(kw['address'].strip())
        h.online_status = DBSession.query(Status)\
                          .filter_by(label='Offline').first()
                          
        res = self._get_geoip_data(h.address)
        if not res:
            errors['host_address'] = "The host '%s' could not be " + \
                                     "identified via GeoIP.  Please " + \
                                     "ensure the hostname resolves" % h.address
        if errors:
            transaction.doom()
            return dict(errors=errors, host=h)

        h.city = unicode(res.get('city', None))
        h.region_name   = unicode(res.get('region_name', None))
        h.longitude     = res.get('longitude', None)
        h.latitude      = res.get('latitude', None)
        h.country_name  = unicode(res.get('country_name', None))
        h.country_code  = unicode(res.get('country_code', None))
        h.country_code3 = unicode(res.get('country_code3', None))
        h.postal_code   = res.get('postal_code', None)
        flash(_("%s updated successfully!" % kw['address']), 'info')
        redirect(url('/dashboard'))


    @expose('dmirr.templates.%s.delete_wrapper' % config['theme'])
    def delete(self, host_address=None, *a, **kw):
        h = DBSession.query(Host).filter_by(address=host_address).first()   
        if not h:
            raise HTTPNotFound
        _host_address = h.address
        _h.protect_obj(h)
            
        confirmed = kw.get('confirmed', None)        
        if not confirmed:
            display_name = h.address
            action = url('/host/%s/delete' % h.address)
            came_from = url('/host/%s/edit' % h.address)
            return dict(errors={}, display_name=display_name, action=action, 
                        came_from=came_from)
        else:
            DBSession.delete(h)
            transaction.commit()
            flash(_("%s and all associated data have been deleted." % \
                _host_address), 'info')
            redirect(url('/dashboard'))
