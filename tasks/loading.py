from __future__ import print_function, unicode_literals

import ConfigParser
from os import getenv

import luigi
from tasks.transform import StopListText, CreateTokens, CreateTokenLinks
from ops.transform import process_text
from orm.tables import Meetingdate, Token, Tokenlink
from ops.loading import load_token_links_to_db

from . import auth

class InsertTokens(luigi.Task):
    date = luigi.Parameter()

    def requires(self):
        return CreateTokens(self.date)

    def output(self):
        pass

    def run(self):
        engine = connect_engine()
        session = make_session(engine)

        md = session.query(Meetingdate).filter(Meetingdate.date==self.date).all()[0]
        
        with self.input().open('r') as I:
            tokens = pickle.load(I)

            for k,v in tokens.items():
                if k:
                    #TODO: import ORM defs
                    t = Token(token=k, count=v)
                    t.MeetingDate = md
                    session.add(t)

            session.commit()
            session.close()

class InsertTokenLinks(luigi.Task):
    date = luigi.Parameter()

    def requires(self):
        return CreateTokenLinks(self.date)

    def output(self):
        pass

    def run(self):
        engine = connect_engine()
        session = make_session(engine)

        md = session.query(Meetingdate).filter(Meetingdate.date==self.date).all()[0]
        
        with self.input().open('r') as I:
            links = pickle.load(I)
            load_token_links_to_db(session, links, md)


