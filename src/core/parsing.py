from pyquery import PyQuery as pq
import re

from core.PyBatBase import Aggression, BasicSkills, ExtendedSkills, Fitness,\
    Player, RankingSnapshot

# regexes for parsing league/global ranking info and league positions

# typical string would be "#470 in England<br />#5440 in the World".
# captures both country and global ranking
RANK_PATTERN = re.compile(r"#(\d*).*#(\d*).*", re.DOTALL)
# typical string would be "#1 in VI.20"
# captures league position and league name
POSITION_PATTERN = re.compile(r"#(\d*) in (.*)")


class BatParseException(Exception):
    """ Thrown if an error occurs in parsing HTML """
    pass


def parse_team_id(html):
    """
    Finds the team ID in the document. Works with any club page
    """
    document = pq(html)
    team_id = -1

    # look for an element with ID 'pagetitle' which contains the team ID and
    # name
    for link in document('#pagetitle').find('a').eq(1):
        team_id = int(link.attrib['href'].split("office.asp?teamID=")[1])

    if team_id == -1:
        raise BatParseException("Team ID not found in HTML")

    return team_id


def parse_players(html):
    '''
    Parses players from the given HTML string. If the HTML
    does not contain valid player attributes, a BatParseException is thrown.
    '''
    doc = pq(html)
    
    # check title to see if we have a valid Squad page
    if not len(doc('title')) or doc('title').text() != 'Battrick - Squad':
        raise BatParseException()

    player_id = [int(el.attrib['id'].split('player_')[1])
                 for el in doc('div.player')]

    # record number of players and check we actually have some
    n_players = player_id.__len__()

    if(n_players == 0):
        raise BatParseException("Invalid players HTML.")

    # parse player attributes into lists for each attribute
    player_name = [el.text_content() for el in doc('span.player_name')]
    player_age = [int(el.text_content()) for el in doc('span.player_age')]
    player_btr = [int(el.text_content().replace(',', ''))
                  for el in doc('span.player_btr')]
    player_wage = [int(el.text_content().replace(',', '').replace('£', ''))
                   for el in doc('span.player_wage')]
    player_aggression = [Aggression[el.text_content()]
                         for el in doc('span.player_aggression')]
    player_bathand = [el.text_content() for el in doc('span.player_bathand')]
    player_aggressionbowl = [
        Aggression[el.text_content()] for el in doc('span.player_aggressionbowl')]
    player_bowlhand = [el.text_content() for el in doc('span.player_bowlhand')]
    player_leadership = [BasicSkills[el.text_content()]
                         for el in doc('span.player_leadership')]
    player_experience = [ExtendedSkills[el.text_content()]
                         for el in doc('span.player_experience > a')]
    player_batform = [BasicSkills[el.text_content()]
                      for el in doc('span.player_batform')]
    player_bowlform = [BasicSkills[el.text_content()]
                       for el in doc('span.player_bowlform')]
    player_fitness = [Fitness[el.text_content()]
                      for el in doc('span.player_fitness')]
    player_stamina = [BasicSkills[el.text_content()]
                      for el in doc('span.player_stamina')]
    player_batting = [ExtendedSkills[el.text_content()]
                      for el in doc('span.player_batting')]
    player_keeping = [ExtendedSkills[el.text_content()]
                      for el in doc('span.player_keeping')]
    player_concentration = [
        ExtendedSkills[el.text_content()] for el in doc('span.player_concentration')]
    player_bowling = [ExtendedSkills[el.text_content()]
                      for el in doc('span.player_bowling')]
    player_consistency = [ExtendedSkills[el.text_content()]
                          for el in doc('span.player_consistency')]
    player_fielding = [ExtendedSkills[el.text_content()]
                       for el in doc('span.player_fielding')]

    # and now loop through lists and assign attributes to players
    players = []

    for i in range(0, n_players):
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


def __parse_league_snippet__(element):
    """ Parses league position, name and ID from a HTML element """
    matches = POSITION_PATTERN.search(element.text_content())
    pos = int(matches.group(1))
    name = matches.group(2)
    league_id = int(element.getchildren()[0].attrib['href'].split('=')[1])
    return pos, name, league_id


def parse_pavilion(html):
    """
    Parses a Pavilion HTML string, parsing country/global rankings and league positions
    """
    doc = pq(html)
    if len(doc('title')) == 0 or doc('title').text() != 'Battrick - Pavilion':
        raise BatParseException()
    ranking = RankingSnapshot()

    for tr in doc('tr'):
        for el in tr.getchildren():
            text = el.text_content()

            if(text.startswith('First')):
                (ranking.fcLeaguePos,
                 ranking.fcLeagueName,
                 ranking.fcLeagueID) = __parse_league_snippet__(el.getnext())
            elif(text.startswith('One')):
                (ranking.odLeaguePos, ranking.odLeagueName,
                 ranking.odLeagueID) = __parse_league_snippet__(el.getnext())
            elif(text.startswith('BT20')):
                (ranking.bt20LeaguePos, ranking.bt20LeagueName,
                 ranking.bt20LeagueID) = __parse_league_snippet__(el.getnext())
            elif(text.startswith('Team')):
                matches = RANK_PATTERN.search(el.getnext().text_content())
                ranking.countryR = int(matches.group(1))
                ranking.globalR = int(matches.group(2))

    return ranking
