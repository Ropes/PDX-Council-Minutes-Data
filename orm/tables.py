from __future__ import print_function, unicode_literals

from pprint import pformat
from sqlalchemy import Column, Integer, String, Date, DateTime, MetaData

from .conn import connect_engine, declare_base 

Base = declare_base()

class MinutesTokens(Base):
    __tablename__ = 'MinutesTokens'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    created_on = Column(DateTime)
    token = Column(String(50))
    token_stemmed = Column(String(50))

