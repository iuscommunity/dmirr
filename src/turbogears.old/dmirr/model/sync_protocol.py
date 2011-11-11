# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from dmirr.model import DeclarativeBase, metadata, DBSession


class SyncProtocol(DeclarativeBase):
    __tablename__ = 'sync_protocols'
    
    #{ Columns
    
    id = Column(Integer, primary_key=True)
    
    label = Column(Unicode(255), nullable=False)
    
    command = Column(Unicode(255), nullable=False)
    
    default_flags = Column(Unicode(255), nullable=True
    )
    #}
