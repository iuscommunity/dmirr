# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from tg.exceptions import HTTPNotFound
import datetime

from dmirr.model import DeclarativeBase, metadata, DBSession
from dmirr.model.status import Status
from dmirr.model.project import Project
from dmirr.model.site import Site


host_site_table = Table('host_site_assignments', metadata,
    Column('host_id', Integer, ForeignKey('hosts.id',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('site_id', Integer, ForeignKey('sites.id',
        onupdate="CASCADE", ondelete="CASCADE"))
)

host_project_table = Table('host_project_assignments', metadata,
    Column('host_id', Integer, ForeignKey('hosts.id',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('project_id', Integer, ForeignKey('projects.id',
        onupdate="CASCADE", ondelete="CASCADE"))

)


class Host(DeclarativeBase):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True)
    address = Column(Unicode(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('tg_user.user_id'), nullable=False)
    group_id = Column(Integer, ForeignKey('tg_group.group_id'), nullable=True)
    online_status_id = Column(Integer, ForeignKey('status.id'), nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)

    # geoip data
    city = Column(Unicode(64), nullable=True)
    region_name = Column(Unicode(64), nullable=True)
    longitude = Column(Integer, nullable=True)
    latitude = Column(Integer, nullable=True)
    country_name = Column(Unicode(64), nullable=True)
    country_code3 = Column(Unicode(3), nullable=True)
    country_code = Column(Unicode(2), nullable=True)
    postal_code = Column(Integer, nullable=True)
    
    # objects
    online_status = relation('Status', uselist=False, backref='host')
    projects = relation('Project', order_by='Project.display_name', secondary=host_project_table, backref='hosts')
    sites = relation('Site', order_by='Site.display_name', secondary=host_site_table, backref='hosts')
    
    @property
    def location(self):
        if self.city and self.region_name and self.country_name:
            location = "%s, %s - %s" % (self.city, self.region_name, 
                                      self.country_name)
        elif self.region_name and self.country_name:
            location = "%s - %s" % (self.region_name, self.country_name)
        elif self.country_name:
            location = "unknown - %s" % self.country_name
        else:
            location = 'unknown'
        return location
