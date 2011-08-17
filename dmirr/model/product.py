# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from dmirr.model import DeclarativeBase, metadata, DBSession
from tg.exceptions import HTTPNotFound
import datetime

release_arch_table = Table('release_arch_assignments', metadata,
    Column('product_release_id', Integer, ForeignKey('product_releases.id',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('arch_id', Integer, ForeignKey('archs.id',
        onupdate="CASCADE", ondelete="CASCADE"))
)

class Arch(DeclarativeBase):
    __tablename__ = 'archs'
    id = Column(Integer, primary_key=True)
    label = Column(Unicode(8), unique=True, nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    
    def __repr__(self):
        return '<Arch: label=%s>' % self.label
    
    def __unicode__(self):
        return self.label
        
class Product(DeclarativeBase):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    label = Column(Unicode(32), unique=True, nullable=False)
    display_name = Column(Unicode(64), nullable=True)
    desc = Column(Unicode(255), nullable=True)
    project_id = Column(Integer, 
        ForeignKey('projects.id', onupdate="CASCADE", ondelete="CASCADE"), 
        nullable=True
        )
    group_id = Column(Integer, ForeignKey('tg_group.group_id'), 
                    nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow(), 
                    nullable=False)
    releases = relation('ProductRelease', 
                    order_by='ProductRelease.display_name', backref='product', 
                    cascade='all')
    
class ProductRelease(DeclarativeBase):
    __tablename__ = 'product_releases'
    id = Column(Integer, primary_key=True)
    label = Column(Unicode(32), unique=True, nullable=False)
    display_name = Column(Unicode(64), nullable=True)
    desc = Column(Unicode(255), nullable=True)
    path = Column(Unicode(255), nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    product_id = Column(Integer, 
        ForeignKey('products.id', onupdate="CASCADE", ondelete="CASCADE"), 
        nullable=True
        )
    #product = relation('Product', order_by='ProductRelease.display_name', backref='releases')
    # special
    archs = relation('Arch', order_by='Arch.label', 
                secondary=release_arch_table, backref='product_releases')
