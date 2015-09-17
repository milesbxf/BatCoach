from nose.tools import assert_equal, assert_is, raises
from os import path
from posix import getcwd
from unittest.case import TestCase

from core.parsing import parse_players, BatParseException, parse_pavilion,\
    parse_team_id


@raises(BatParseException)
def test_parse_players_throws_BatParseException_if_no_player_info():
    parse_players('html with no player info')


@raises(BatParseException)
def test_parse_pavilion_throws_BatParseException_if_no_pavilion_info():
    parse_pavilion('html with no pavilion info')


def test_parse_team_id_parses_id():
    file = open(
            path.join(getcwd(), 'test', 'resources', 'squad.html'), 'r'
        )
    html = file.read()
    teamID = parse_team_id(html)
    assert_equal(teamID, 30438)

class TestParsingPlayer():
    """
    Tests for parsing player attributes and information from a HTML file.
    """

    @classmethod
    def setUpClass(cls):
        file = open(
            path.join(getcwd(), 'test', 'resources', 'squad.html'), 'r'
        )
        html = file.read()
        cls.players = parse_players(html)
        cls.p = cls.players[0]
        file.close()

    def test_parses_enough_players(self):
        assert_equal(len(self.players), 16)

    def test_parses_id(self):
        assert_equal(self.p.id, 4947072)

    def test_parses_name(self):
        assert_equal(self.p.name, "Duke Benton")

    def test_parses_age(self):
        assert_equal(self.p.age, 17)

    def test_parses_btr(self):
        assert_equal(self.p.btr, 4531)

    def test_parses_wage(self):
        assert_equal(self.p.wage, 434)

    def test_parses_aggression(self):
        assert_equal(self.p.aggression, 3)

    def test_parses_bathand(self):
        assert_equal(self.p.bathand, "R")

    def test_parses_aggressionbowl(self):
        assert_equal(self.p.aggressionbowl, 1)

    def test_parses_bowlhand(self):
        assert_equal(self.p.bowlhand, "R")

    def test_parses_leadership(self):
        assert_equal(self.p.leadership, 4)

    def test_parses_experience(self):
        assert_equal(self.p.experience, 1)

    def test_parses_batform(self):
        assert_equal(self.p.batform, 9)

    def test_parses_bowlform(self):
        assert_equal(self.p.bowlform, 6)

    def test_parses_fitness(self):
        assert_equal(self.p.fitness, 7)

    def test_parses_stamina(self):
        assert_equal(self.p.stamina, 5)

    def test_parses_batting(self):
        assert_equal(self.p.batting, 5)

    def test_parses_keeping(self):
        assert_equal(self.p.keeping, 2)

    def test_parses_concentration(self):
        assert_equal(self.p.concentration, 5)

    def test_parses_bowling(self):
        assert_equal(self.p.bowling, 1)

    def test_parses_consistency(self):
        assert_equal(self.p.consistency, 5)

    def test_parses_fielding(self):
        assert_equal(self.p.fielding, 3)


class TestParsingPavilion():
    """
    Tests parsing of a pavilion file.
    """

    @classmethod
    def setUpClass(cls):
        file = open(
            path.join(getcwd(), 'test', 'resources', 'pavilion.html'), 'r'
        )
        html = file.read()
        cls.ranking = parse_pavilion(html)
        file.close()

    def test_parses_FC_league_pos(self):
        assert_equal(self.ranking.fcLeaguePos, 4)

    def test_parses_FC_league_name(self):
        assert_equal(self.ranking.fcLeagueName, 'VIII.20')

    def test_parses_FC_league_ID(self):
        assert_equal(self.ranking.fcLeagueID, 12273)

    def test_parses_OD_league_pos(self):
        assert_equal(self.ranking.odLeaguePos, 5)

    def test_parses_OD_league_name(self):
        assert_equal(self.ranking.odLeagueName, 'V.195')

    def test_parses_OD_league_ID(self):
        assert_equal(self.ranking.odLeagueID, 12192)

    def test_parses_BT20_league_pos(self):
        assert_equal(self.ranking.bt20LeaguePos, 4)

    def test_parses_BT20_league_name(self):
        assert_equal(self.ranking.bt20LeagueName, 'VI.606')

    def test_parses_BT20_league_ID(self):
        assert_equal(self.ranking.bt20LeagueID, 8407)

    def test_parses_countryR(self):
        assert_equal(self.ranking.countryR, 1189)

    def test_parses_globalR(self):
        assert_equal(self.ranking.globalR, 12943)
