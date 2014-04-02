from __future__ import print_function, unicode_literals

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tasks.auth import auth

conn_str = 'postgresql+psycopg2://{user}:{password}@{host}/{database}'

def connect_engine():
    x = conn_str.format(user=auth['user'],\
                    password=auth['password'], host='localhost',\
                    database=auth['database'])
    engine = create_engine(x)
    return engine

def declare_base():
    Base = declarative_base() 
    return Base

def make_session(engine):
    return sessionmaker(bind=engine)

