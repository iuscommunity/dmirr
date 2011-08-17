# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from dmirr.model import DeclarativeBase, metadata, DBSession
from dmirr.model.product import Product
from dmirr.model.sync_protocol import SyncProtocol
from dmirr.model.site import Site
import datetime

site_project_table = Table('site_project_assignments', metadata,
    Column('site_id', Integer, ForeignKey('sites.id',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('project_id', Integer, ForeignKey('projects.id',
        onupdate="CASCADE", ondelete="CASCADE"))
)


class Project(DeclarativeBase):
    __tablename__ = 'projects'
    
    #{ Columns
    
    id = Column(Integer, unique=True, primary_key=True)
    label = Column(Unicode(16), unique=True, nullable=False)
    display_name = Column(Unicode(64), nullable=False)
    desc = Column(String(255), nullable=True)
    url = Column(Unicode(255), nullable=True)
    # upstream_host = Column(Unicode(255), nullable=False)
    sync_base_path = Column(Unicode(255), nullable=False)
    sync_flags = Column(Unicode(255), nullable=True)
    sync_protocol_id = Column(Integer, ForeignKey('sync_protocols.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('tg_user.user_id'), nullable=False)
    group_id = Column(Integer, ForeignKey('tg_group.group_id'), nullable=True)
    private = Column(Boolean, nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    
    # relations
    products = relation('Product', order_by='Product.display_name', backref='project', cascade='all,delete-orphan')
    sync_protocol = relation(SyncProtocol, uselist=False, backref='project')
    
    sites = relation('Site', order_by='Site.display_name', secondary=site_project_table, backref='projects')
    
    #}
    def _sync_path(self, site_id):
        sync_path = DBSession.query(SiteSyncPath).filter_by(project_id=self.id)\
                    .filter_by(site_id=site_id).first()
        return sync_path.sync_path
        
class SiteSyncPath(DeclarativeBase):
    __tablename__ = 'site_sync_paths'
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    sync_path = Column(Unicode(255), nullable=False)
    
    site = relation('Site', uselist=False, backref='sync_path')
    project = relation('Project', uselist=False, backref='sync_path')
