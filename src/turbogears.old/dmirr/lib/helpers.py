# -*- coding: utf-8 -*-

"""WebHelpers used in dmirr."""

from webhelpers import date, feedgenerator, html, number, misc, text
from repoze.what.predicates import NotAuthorizedError, Any, is_user, \
                                   has_permission, not_anonymous, in_group
from random import choice
import pylons
import hashlib
import random
import string
import datetime

from dmirr.model import DBSession as db
from dmirr import model as model
from pkg_resources import get_distribution

def get_version():
    return get_distribution('dmirr').version
    
def gen_password():
    newpasswd = ''
    chars = string.letters + string.digits
    for i in range(12):
        newpasswd = newpasswd + choice(chars)
    return newpasswd

def gen_verification_code():
    vtxt = "%s%s%s" % (
        random.random(), datetime.datetime.now(), random.random()
        )
    return hashlib.md5(vtxt).hexdigest()
    
def get_validation_errors():
    values = pylons.c.form_values
    errors = {}
    for key, value in pylons.c.form_errors.iteritems():
        errors[key] = value
    return errors

def status_by_name(label=None):
    s = db.query(model.Status).filter_by(label=label).first()
    return s
        
def group_by_name(group_name=None):
    g = db.query(model.Group).filter_by(group_name=group_name).first()
    return g
    
def protect_obj_modify(protected_obj=None):
    p = protected_obj
    if p:
        if not Any(is_user(p.user.user_name), 
                   has_permission('dmirr_admin'), 
                   in_group(p.group.group_name)):
            raise NotAuthorizedError

def protect_user_obj(protected_obj=None):
    p = protected_obj
    if p:
        if not Any(is_user(p.user_name), 
                   has_permission('dmirr_admin')):
            raise NotAuthorizedError

def protect_group_obj(protected_obj=None):
    p = protected_obj
    if p:
        if not Any(is_user(p.owner.user_name), 
                   has_permission('dmirr_admin')):
            raise NotAuthorizedError


def protect_obj(protected_obj=None):
    p = protected_obj
    if p:
        if not Any(is_user(p.user.user_name), 
                   has_permission('dmirr_admin'), 
                   in_group(p.group.group_name)):
            raise NotAuthorizedError

def protect_product_release_obj(protected_obj=None):
    p = protected_obj
    if p:
        if not Any(is_user(p.product.project.user.user_name), 
                   has_permission('dmirr_admin'), 
                   in_group(p.product.project.group.group_name)):
            raise NotAuthorizedError

def get_group_by_name(group_name=None):
    if not group_name:
        group_name = 'dmirr_no_group'
    group = db.query(model.Group)\
            .filter_by(group_name=group_name)\
            .first()
    return group

def get_protocol_by_name(protocol_label=None):
    if not protocol_label:
        protocol_label = 'rsync'
    protocol = db.query(model.SyncProtocol)\
               .filter_by(label=protocol_label).first()
    return protocol

def get_project_by_name(project_label=None):
    project = db.query(model.Project).filter_by(label=project_label).first()
    return project
    
def get_product_by_name(product_label=None):
    product = db.query(model.Product).filter_by(label=product_label).first()
    return product

def get_release_by_name(release_label=None):
    release = db.query(model.ProductRelease).filter_by(label=release_label)\
              .first()
    return release

def get_site_by_name(site_label=None):
    release = db.query(model.Site).filter_by(label=site_label)\
              .first()
    return release
    
def get_host_by_address(host_address=None):
    host = db.query(model.Host).filter_by(address=host_address).first()
    return host
