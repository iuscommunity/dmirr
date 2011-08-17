# -*- coding: utf-8 -*-
"""Setup the dmirr application"""

import logging
import sys
import transaction
from tg import config

from dmirr.config.environment import load_environment
import datetime

__all__ = ['setup_app']

log = logging.getLogger(__name__)

STATUS = [
    'Enabled', 
    'Disabled', 
    'Online', 
    'Offline', 
    'Current', 
    'OutOfDate',
    'PendingEmailVerification'
    ]

PROTOCOLS = {
    'rsync' : ('rsync', '-a --delete'),
    'http' : ('wget', ''),
    'https' : ('wget', ''),
    'ftp' : ('wget', '')
    }
    
def setup_app(command, conf, vars):
    """Place any commands to setup dmirr here"""
    load_environment(conf.global_conf, conf.local_conf)
    # Load the models
    from dmirr import model
    print "Creating tables"
    model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)

    # default archs
    for arch in [u'i386', u'x86_64', u'ppc', u'ppc64']:
        a = model.Arch()
        a.label = arch
        model.DBSession.add(a)
        model.DBSession.flush()
    
    # status
    for status in STATUS:
        s = model.Status()
        s.label = status
        model.DBSession.add(s)
        model.DBSession.flush()
                
    # protocols
    for protocol in PROTOCOLS:
        p = model.SyncProtocol()
        p.label = protocol
        p.command = PROTOCOLS[protocol][0]
        p.default_flags = PROTOCOLS[protocol][1]
        model.DBSession.add(p)
        model.DBSession.flush()
    
    transaction.commit()
        
    manager = model.User()
    manager.user_name = u'admin'
    manager.display_name = u'dMirr Administrator'
    manager.email_address = u'admin@localhost'
    manager.status = model.DBSession.query(model.Status)\
                     .filter_by(label="Enabled").first()
    manager.password = u'dmirr'

    model.DBSession.add(manager)
    model.DBSession.flush()
    
    group = model.Group()
    group.group_name = u'dmirr_admin'
    group.owner = manager
    group.display_name = u'dMirr Global Administrators Group'

    group.users.append(manager)

    model.DBSession.add(group)
    
    no_group = model.Group()
    no_group.group_name = u'dmirr_no_group'
    no_group.owner = manager
    no_group.display_name = u'No Group'
    model.DBSession.add(no_group)
    
    users_group = model.Group()
    users_group.group_name = u'dmirr_everyone'
    users_group.owner = manager
    users_group.display_name = u'All dMirr Users'
    users_group.users.append(manager)
    model.DBSession.add(users_group)
    
    # perms            
    permission = model.Permission()
    permission.permission_name = u'dmirr_admin'
    permission.description = u'This permission give an administrative right to the bearer'
    permission.groups.append(group)
    model.DBSession.add(permission)
    model.DBSession.flush()

    permission = model.Permission()
    permission.permission_name = u'dmirr_project'
    permission.description = u'Ability to create, modify, delete projects.'
    permission.groups.append(group)
    permission.groups.append(users_group)
    model.DBSession.add(permission)
    model.DBSession.flush()
    
    permission = model.Permission()
    permission.permission_name = u'dmirr_site'
    permission.description = u'Ability to create, modify, delete sites.'
    permission.groups.append(group)
    permission.groups.append(users_group)
    model.DBSession.add(permission)
    model.DBSession.flush()

    permission = model.Permission()
    permission.permission_name = u'dmirr_host'
    permission.description = u'Ability to create, modify, delete hosts.'
    permission.groups.append(group)
    permission.groups.append(users_group)
    model.DBSession.add(permission)
    model.DBSession.flush()

    permission = model.Permission()
    permission.permission_name = u'dmirr_group'
    permission.description = u'Ability to create, modify, delete groups.'
    permission.groups.append(group)
    permission.groups.append(users_group)
    model.DBSession.add(permission)
    model.DBSession.flush()
        
    transaction.commit()
        
    project = model.Project()
    project.label = u'example'
    project.display_name = u'My Example Project'
    project.desc = u"This is a sample project."
    project.url = u"http://www.example.com"
    project.user = manager
    # project.upstream_host = "origin.example.com"
    project.sync_base_path= u"/pub/example"
    project.sync_flags = u""
    project.sync_protocol = model.DBSession.query(model.SyncProtocol).filter_by(label='rsync').first()
    project.group = no_group
    model.DBSession.add(project)
    model.DBSession.flush()
    
    site = model.Site()
    site.label = u'mysite'
    site.display_name = u'My Site'
    site.url = u'http:/mysite.example.com'
    site.contact_name = u'My Site Admin'
    site.contact_email = u'admin@mysite.example.com'
    site.sync_base_path = u'/pub/'
    site.user = manager
    site.group = no_group
    model.DBSession.add(site)
    model.DBSession.flush()
    
    product = model.Product()
    product.label = u'mydistro'
    product.display_name = u"My Distro"
    product.desc = u"This is a sample product, most commonly a linux distribution."
    product.project = project
    model.DBSession.add(product)
    model.DBSession.flush()
    
    release = model.ProductRelease()
    release.label = u'mydistro-5'
    release.display_name = u'My Distro 5'
    release.desc = u'This is a sample release, version 5 of the My Distro product.'
    release.arch = model.DBSession.query(model.Arch).filter_by(label='i386').first()
    release.path = u'/mydistro/5/i386'
    release.product = product
    model.DBSession.add(release)
    model.DBSession.flush()
    
    transaction.commit()
    print "Successfully setup"
