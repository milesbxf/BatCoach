import sqlalchemy
from core import Base
from sqlalchemy.orm.session import sessionmaker
from core.PyBatBase import HTMLFile, page_types, PageTypes, Team
from core.parsing import BatParseException, parse_players, parse_pavilion, parse_team_id
from pyquery import PyQuery as pq
import os
from _datetime import datetime
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError


class BatDatabaseError(Exception):
    pass


class Model():

    def __init__(self, dbcon='sqlite:///:memory:', echo=False):
        self.engine = sqlalchemy.create_engine(dbcon, echo=echo)

        # create tables
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)

        with self.session_scope() as session:
            print(session.query(Team).count())

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def import_multiple_files(self,files):
        html_files = []
        with self.session_scope() as session:
            for file in files:
                html_files.append(self.import_file(file, session))
        return html_files

    def import_file(self, html_file,session):

        team = None
        
        for t in Base.metadata.sorted_tables:
            print(t.name)
        
        team_id = parse_team_id(html_file.HTML)
        
        result = session.query(Team).filter_by(id=team_id)

        if(result.count()):
            team = result.first()
        else:
            raise BatDatabaseError(
                "Team with ID %d not found in the database" % team_id)

        # pass the html to the appropriate parsing function
        if(html_file.type == PageTypes.Pavilion.value):
            ranking = parse_pavilion(html_file.HTML)
        elif(html_file.type == PageTypes.Squad.value):
            team.players = parse_players(html_file.HTML)

        session.add(team)
        session.add(html_file)
        session.flush()
#             except SQLAlchemyError as err:
#                 raise BatDatabaseError() from err
        return html_file


    def has_teams(self):
        
        with self.session_scope() as session:
        
            result = session.query(Team)
            
            return result.count() > 0
        
        
        