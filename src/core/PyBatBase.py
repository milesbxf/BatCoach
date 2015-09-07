from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum

Base = declarative_base()

print("Loading base classes")

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer,ForeignKey('teams.id'))
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

class RankingSnapshot(Base):
    __tablename__ = 'rankings'
    id = Column(Integer, Sequence('ranking_seq'), primary_key=True)
    date = Column(DateTime)
    team_id = Column(Integer,ForeignKey('teams.id'))
    fcLeagueID = Column(Integer)
    fcLeagueName= Column(String)
    fcLeaguePos = Column(Integer)
    odLeagueID = Column(Integer)
    odLeagueName= Column(String)
    odLeaguePos = Column(Integer)
    bt20LeagueID = Column(Integer)
    bt20LeagueName= Column(String)
    bt20LeaguePos = Column(Integer)
    countryR = Column(Integer)
    globalR = Column(Integer)
    
class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    players = relationship("Player",order_by="Player.id",backref="team")
    rankings = relationship("RankingSnapshot", order_by="RankingSnapshot.date",backref="team")
    
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
    