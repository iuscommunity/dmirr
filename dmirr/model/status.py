# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from dmirr.model import DeclarativeBase, metadata, DBSession

class Status(DeclarativeBase):
    __tablename__ = 'status'
    
    #{ Columns
    
    id = Column(Integer, primary_key=True)
    
    label = Column(Unicode(255), nullable=False)
    
    #}

def status_by_name(label=None):
    s = DBSession.query(Status).filter_by(label=label).first()
    return s
        
