"""
Maintains, updates and provides access to the database.
"""


import sqlalchemy
from core import Base
from sqlalchemy.orm.session import sessionmaker
from core.PyBatBase import PageTypes, Team
from core.parsing import (parse_players,
                          parse_pavilion, parse_team_id)
from contextlib import contextmanager
import cherrypy


class BatDatabaseError(Exception):
    """
    Indicates that an BatCoach specific database error has occurred, e.g.
    a teamID has not been found in the database.
    """
    pass


class Model():
    """
    Provides database access to the BatCoach application through a single
    entry point, mediating importing and parsing of files.
    """

    def __init__(self, dbcon='sqlite:///:memory:', echo=False):
        """ 
        Initialises a new Model, creating a new database connection (specified by dbcon).
        Echo: whether SQLAlchemy outputs debug information to the console.
        """
        self.engine = sqlalchemy.create_engine(dbcon, echo=echo)

        # if tables aren't already present, create them
        Base.metadata.create_all(self.engine)

        # base class for database sessions
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def session_scope(self):
        """
        Provide a transactional scope around a series of operations.
        If exceptions occur the changes are rolled back, otherwise they are
        committed.
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def import_file(self, html_file):
        """
        Imports a single HTMLFile into the database, parsing as appropriate.
        The team is created if it doesn't already exist
        """
        team = None

        with self.session_scope() as session:
            # find team in the database
            team_id = parse_team_id(html_file.HTML)
            result = session.query(Team).filter_by(id=team_id)

            if(result.count()):
                team = result.first()
            else:  # no team, so create it
                team = Team()
                team.id = team_id

            # pass the html to the appropriate parsing function
            if(html_file.type == PageTypes.Pavilion.value):
                team.add_ranking(parse_pavilion(html_file.HTML))
            elif(html_file.type == PageTypes.Squad.value):
                team.players = parse_players(html_file.HTML)

            # add the team and HTML file to the database
            session.add(team)
            session.add(html_file)
            session.flush()

        return html_file

    def get_team(self, session=None):
        if session is None:
            with self.session_scope() as new_session:
                return self.get_team(new_session)
        return session.query(Team).first()

    def get_players(self, session=None):
        if session is None:
            with self.session_scope() as new_session:
                return self.get_players(new_session)
        team = self.get_team(session)
        return team.players

    def has_teams(self):
        """
        Checks whether any teams are defined in the database.
        """

        with self.session_scope() as session:
            result = session.query(Team)
            return result.count() > 0
