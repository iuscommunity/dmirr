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


    
class Site(DeclarativeBase):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)
    label = Column(Unicode(32), unique=True, nullable=False)
    display_name = Column(Unicode(128), nullable=False)
    desc = Column(Unicode(255), nullable=True)
    url = Column(Unicode(255), nullable=True)
    private = Column(Boolean, nullable=True)
    sync_base_path = Column(Unicode(255), nullable=False)
    contact_name = Column(Unicode(64), nullable=True)
    contact_email = Column(Unicode(255), nullable=True)
    user_id = Column(Integer, ForeignKey('tg_user.user_id'), nullable=False)
    group_id = Column(Integer, ForeignKey('tg_group.group_id'), nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
        
