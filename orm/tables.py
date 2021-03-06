# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Meetingdate(Base):
    __tablename__ = 'MeetingDate'
    __table_args__ = (
        Index('MeetingDate_id_date_key', 'id', 'date'),
    )

    id = Column(BigInteger, primary_key=True)
    date = Column(Date, nullable=False, unique=True)


class Token(Base):
    __tablename__ = 'Token'
    __table_args__ = (
        Index('Token_token_dateid_key', 'token', 'dateid'),
    )

    tokenid = Column(BigInteger, primary_key=True)
    count = Column(Integer, nullable=False, server_default=u'0')
    dateid = Column(ForeignKey('MeetingDate.id'))
    token = Column(String(50))

    MeetingDate = relationship(u'Meetingdate')


class Tokenlink(Base):
    __tablename__ = 'TokenLinks'
    __table_args__ = (
        Index('TokenLinks_source_target_index_distance_dateid_key', 'source', 'target', 'index', 'distance', 'dateid'),
    )

    dateid = Column(ForeignKey('MeetingDate.id'), nullable=False)
    source = Column(ForeignKey('Token.tokenid'), nullable=False)
    target = Column(ForeignKey('Token.tokenid'), nullable=False)
    distance = Column(Integer, nullable=False)
    index = Column(Integer, nullable=False)
    linkid = Column(BigInteger, primary_key=True)

    MeetingDate = relationship(u'Meetingdate')
    Token = relationship(u'Token', primaryjoin='Tokenlink.source == Token.tokenid')
    Token1 = relationship(u'Token', primaryjoin='Tokenlink.target == Token.tokenid')
