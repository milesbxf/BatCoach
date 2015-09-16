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

    def import_file(self, file,session):

        # read in the file
        html_file = self.__read_file__(file)

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

    def __read_file__(self, file, commit_to_db=True):

        htmlFile = HTMLFile()

        try:
            # open the file and read into a PyQuery Document
            f = open(file, 'r')
            html = f.read()
            doc = pq(html)

            title_text = doc('title').text()

            # check that this page has a title we can check

            if not title_text:
                raise BatParseException("Empty <title>")
            elif not title_text.startswith('Battrick - '):
                raise BatParseException(
                    "<title>%s</title is not a valid Battrick title" %
                    title_text)

            # extract page information from title
            pagetype = title_text.split(sep='Battrick - ')[1]

            try:
                htmlFile.type = page_types[pagetype].value
            except KeyError:
                raise BatParseException(
                    "Page type '%s' not valid or not currently supported" % pagetype)

            # add modified and imported time
            htmlFile.date_modified = datetime.fromtimestamp(
                os.path.getmtime(file))
            htmlFile.date_imported = datetime.today()

            # add HTML
            htmlFile.HTML = html

        finally:
            f.close()

        return htmlFile

    def has_teams(self):
        
        with self.session_scope() as session:
        
            result = session.query(Team)
            
            return result.count() > 0
        
        
        