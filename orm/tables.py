# coding: utf-8
from sqlalchemy import Column, Date, ForeignKey, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Meetingdate(Base):
    __tablename__ = 'MeetingDate'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)


class Token(Base):
    __tablename__ = 'Token'

    tokenid = Column(Integer, primary_key=True, nullable=False)
    token = Column(String(50))
    count = Column(Integer, nullable=False, server_default=u'0')
    dateid = Column(ForeignKey(u'MeetingDate.id'), nullable=False)

    MeetingDate = relationship(u'Meetingdate')


class Tokenlink(Base):
    __tablename__ = 'TokenLinks'

    linkid = Column(Integer, primary_key=True)
    dateid = Column(ForeignKey('MeetingDate.id'), nullable=False)
    source = Column(ForeignKey('Token.tokenid'), nullable=False)
    target = Column(ForeignKey('Token.tokenid'), nullable=False)
    distance = Column(Integer, nullable=False)

    MeetingDate = relationship(u'Meetingdate')
    Token = relationship(u'Token', primaryjoin='Tokenlink.source == Token.tokenid')
    Token1 = relationship(u'Token', primaryjoin='Tokenlink.target == Token.tokenid')
