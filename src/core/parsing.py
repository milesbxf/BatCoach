from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,DateTime,Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship, backref
from pyquery import PyQuery as pq
import locale
from core.PyBatBase import *
# import parsing
import re

rankPat = re.compile("#(\d*).*#(\d*).*",re.DOTALL)
posPat = re.compile("#(\d*) in (.*)")

def parseTeamID(document):
    teamID = -1;
    for link in document('a[href^="office.asp?teamID="]'):
        id = link.attrib['href'].split("office.asp?teamID=")[1]
        if(not id.startswith('-')):
            teamID = id
    return teamID

def parsePlayers(html):
    
    doc = pq(html)
    
    player_id = [int(el.attrib['id'].split('player_')[1]) for el in doc('div.player')]
    player_name = [el.text_content() for el in doc('span.player_name')]
    player_age = [int(el.text_content()) for el in doc('span.player_age')]
    player_btr = [int(el.text_content().replace(',','')) for el in doc('span.player_btr')]
    player_wage = [int(el.text_content().replace(',','').replace('£','')) for el in doc('span.player_wage')]
    player_aggression = [Aggression[el.text_content()] for el in doc('span.player_aggression')]
    player_bathand = [el.text_content() for el in doc('span.player_bathand')]
    player_aggressionbowl = [Aggression[el.text_content()] for el in doc('span.player_aggressionbowl')]
    player_bowlhand = [el.text_content() for el in doc('span.player_bowlhand')]
    player_leadership = [BasicSkills[el.text_content()] for el in doc('span.player_leadership')]
    player_experience = [ExtendedSkills[el.text_content()] for el in doc('span.player_experience > a')]
    player_batform = [BasicSkills[el.text_content()] for el in doc('span.player_batform')]
    player_bowlform = [BasicSkills[el.text_content()] for el in doc('span.player_bowlform')]
    player_fitness = [Fitness[el.text_content()] for el in doc('span.player_fitness')]
    player_stamina = [BasicSkills[el.text_content()] for el in doc('span.player_stamina')]
    player_batting = [ExtendedSkills[el.text_content()] for el in doc('span.player_batting')]
    player_keeping = [ExtendedSkills[el.text_content()] for el in doc('span.player_keeping')]
    player_concentration = [ExtendedSkills[el.text_content()] for el in doc('span.player_concentration')]
    player_bowling = [ExtendedSkills[el.text_content()] for el in doc('span.player_bowling')]
    player_consistency = [ExtendedSkills[el.text_content()] for el in doc('span.player_consistency')]
    player_fielding = [ExtendedSkills[el.text_content()] for el in doc('span.player_fielding')]
    
    players = []
    
    for i in range(0,player_id.__len__()):
        p = Player()
        
        p.id = player_id[i]
        p.name = player_name[i]
        p.age = player_age[i]
        p.btr = player_btr[i]
        p.wage = player_wage[i]
        p.aggression = player_aggression[i].value
        p.bathand = player_bathand[i]
        p.aggressionbowl = player_aggressionbowl[i].value
        p.bowlhand = player_bowlhand[i]
        p.leadership = player_leadership[i].value
        p.experience = player_experience[i].value
        p.batform = player_batform[i].value
        p.bowlform = player_bowlform[i].value
        p.fitness = player_fitness[i].value
        p.stamina = player_stamina[i].value
        p.batting = player_batting[i].value
        p.keeping = player_keeping[i].value
        p.concentration = player_concentration[i].value
        p.bowling = player_bowling[i].value
        p.consistency = player_consistency[i].value
        p.fielding = player_fielding[i].value
        
        players.append(p)
        
    return players

def parseLeagueSnippet(element):
    matches = posPat.search(element.text_content())
    pos = int(matches.group(1))
    name = matches.group(2)
    id = int(element.getchildren()[0].attrib['href'].split('=')[1])
    return (pos,name,id)

def parsePavilion(doc):
    
    ranking = RankingSnapshot()
            
    for tr in doc('tr'):
        for el in tr.getchildren():
            text = el.text_content()
            
            if(text.startswith('First')):
                ranking.fcLeaguePos,ranking.fcLeagueName,ranking.fcLeaguePos = parseLeagueSnippet(el.getnext())
            elif(text.startswith('One')):
                ranking.odLeaguePos,ranking.odLeagueName,ranking.odLeaguePos = parseLeagueSnippet(el.getnext())
            elif(text.startswith('BT20')):
                ranking.bt20LeaguePos,ranking.bt20LeagueName,ranking.bt20LeagueID = parseLeagueSnippet(el.getnext())
            elif(text.startswith('Team')):
                matches = rankPat.search(el.getnext().text_content())
                ranking.countryR = int(matches.group(1))
                ranking.globalR = int(matches.group(2))
    
    return ranking