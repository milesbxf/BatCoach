from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum
from core import Base

from pyquery import PyQuery as pq
from datetime import datetime
import os

class PageParseException(Exception):
    pass


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    name = Column(String)
    age = Column(Integer)
    btr = Column(Integer)
    wage = Column(Integer)
    aggression = Column(Integer)
    bathand = Column(String)
    aggressionbowl = Column(Integer)
    bowlhand = Column(String)
    leadership = Column(Integer)
    experience = Column(Integer)
    batform = Column(Integer)
    bowlform = Column(Integer)
    fitness = Column(Integer)
    stamina = Column(Integer)
    batting = Column(Integer)
    keeping = Column(Integer)
    concentration = Column(Integer)
    bowling = Column(Integer)
    consistency = Column(Integer)
    fielding = Column(Integer)

    def __str__(self):
        return str(self.__dict__)

    def __hash__(self):
        hashsum = 0
        for key, value in self.__dict__.items():
            hashsum += hash(value)
        return hashsum

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class RankingSnapshot(Base):
    __tablename__ = 'rankings'
    id = Column(Integer, Sequence('ranking_seq'), primary_key=True)
    date = Column(DateTime)
    team_id = Column(Integer, ForeignKey('teams.id'))
    fcLeagueID = Column(Integer)
    fcLeagueName = Column(String)
    fcLeaguePos = Column(Integer)
    odLeagueID = Column(Integer)
    odLeagueName = Column(String)
    odLeaguePos = Column(Integer)
    bt20LeagueID = Column(Integer)
    bt20LeagueName = Column(String)
    bt20LeaguePos = Column(Integer)
    countryR = Column(Integer)
    globalR = Column(Integer)


class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    players = relationship("Player", order_by="Player.id", backref="team")
    rankings = relationship(
        "RankingSnapshot", order_by="RankingSnapshot.date", backref="team")


class HTMLFile(Base):

    @classmethod
    def from_file(cls, filename):
        ''' Constructs a HTMLFile from a file in memory with specified modified time '''


        try:
            # open the file and read into a PyQuery Document
            f = open(filename, 'r')
            file_contents = f.read()
            mtime = datetime.fromtimestamp(os.path.getmtime(filename))
            
            htmlFile = cls.from_memory(file_contents,mtime)
        finally:
            f.close()

        return htmlFile

    @classmethod
    def from_memory(cls,file_contents,modified_time):
        
        htmlFile = cls()

        doc = pq(file_contents)

        title_text = doc('title').text()

        # check that this page has a title we can check

        if not title_text:
            raise PageParseException("Empty <title>")
        elif not title_text.startswith('Battrick - '):
            raise PageParseException(
                "<title>%s</title is not a valid Battrick title" %
                title_text)

        # extract page information from title
        pagetype = title_text.split(sep='Battrick - ')[1]

        try:
            htmlFile.type = page_types[pagetype].value
        except KeyError:
            raise PageParseException(
                "Page type '%s' not valid or not currently supported" % pagetype)

        # add modified and imported time
        htmlFile.date_modified = modified_time
        htmlFile.date_imported = datetime.today()

        # add HTML
        htmlFile.HTML = file_contents

        return htmlFile

    __tablename__ = 'files'
    id = Column(Integer, Sequence('files_seq'), primary_key=True)
    type = Column(Integer)
    date_modified = Column(DateTime)
    date_imported = Column(DateTime)
    HTML = Column(String)


class BasicSkills(Enum):
    useless = 0
    worthless = 1
    abysmal = 2
    woeful = 3
    feeble = 4
    mediocre = 5
    competent = 6
    respectable = 7
    proficient = 8
    strong = 9
    superb = 10


class ExtendedSkills(Enum):
    useless = 0
    worthless = 1
    abysmal = 2
    woeful = 3
    feeble = 4
    mediocre = 5
    competent = 6
    respectable = 7
    proficient = 8
    strong = 9
    superb = 10
    quality = 11
    remarkable = 12
    wonderful = 13
    exceptional = 14
    sensational = 15
    exquisite = 16
    masterful = 17
    miraculous = 18
    phenomenal = 19
    elite = 20


class Aggression(Enum):
    defensive = 0
    cautious = 1
    steady = 2
    attacking = 3
    destructive = 4


class Fitness(Enum):
    exhausted = 0
    drained = 1
    fatigued = 2
    low = 3
    fair = 4
    moderate = 5
    fresh = 6
    lively = 7
    invigorated = 8
    energetic = 9
    sublime = 10


class PageTypes(Enum):
    Pavilion = 0
    Squad = 1

page_types = {'Pavilion': PageTypes.Pavilion, 'Squad': PageTypes.Squad}
