"""
Tests the Model class.
"""

from core.model import Model
import unittest.mock as mock
from os import path
from nose.tools import assert_equal, assert_false, assert_true
from core.PyBatBase import PageTypes, HTMLFile, Team
from unittest.mock import patch
from core.parsing import parse_players

from unittest.case import TestCase
from datetime import datetime
from sqlalchemy.orm.query import Query
from time import mktime
from test import PROJECT_SOURCE_PATH
from sqlalchemy.orm.session import Session


@mock.patch('sqlalchemy.create_engine')
def test_model_creates_engine_and_inits(mock_create_engine):
    """ Tests that a SQLAlchemy engine is created when Model is initialised """
    Model()
    assert mock_create_engine.called


def test_import_file_updates_db_with_players():
    """
    End to end test asserting that a HTML file is parsed and imported into an
    in-memory SQLite database. 
    """
    model = Model(echo=False)

    # open the HTML file
    file = open(
        path.join(PROJECT_SOURCE_PATH, 'test', 'resources', 'squad.html'), 'r'
    )
    html = file.read()
    file.close()

    # parse the players
    players = parse_players(html)

    with model.session_scope() as session:

        # open a session and import our HTML file
        html_file = HTMLFile.from_file(
            path.join(PROJECT_SOURCE_PATH, 'test', 'resources', 'squad.html'))

        model.import_file(html_file)

        # retrieve the team from the database
        # and check that it has imported correctly
        new_team = session.query(Team).first()
        assert_equal(len(new_team.players), len(players))


class TestModel(TestCase):
    """ Tests the model class. """

    def cleanUp(self):
        """ Stops all unittest.mock patch objects """
        for patcher in self.patchers:
            patcher.stop()

    def setUp(self):
        """ Sets up tests and starts mock patchers """

        # mock open(file) and os.path.getmtime(file)
        patcher_open = patch('builtins.open')
        patcher_mtime = patch('os.path.getmtime')
        self.patchers = [patcher_open, patcher_mtime]
        self.addCleanup(self.cleanUp)

        self.mock_open = patcher_open.start()
        self.mock_open.return_value.__enter__ = lambda s: s
        self.mock_open.return_value.__exit__ = mock.Mock()
        self.mock_open.return_value.read.return_value = '<html><title>Battrick - Squad</title></html>'

        self.mock_mtime = patcher_mtime.start()
        self.test_date = datetime(2015, 1, 1, 12, 0, 10)

        self.mock_session = mock.Mock(spec=Session)

        self.mock_mtime.return_value = mktime(
            self.test_date.timetuple()) + 1e-6 * self.test_date.microsecond

        self.model = Model(echo=False)

    @mock.patch('core.model.parse_players')
    @mock.patch('sqlalchemy.orm.query.Query.count')
    @mock.patch('sqlalchemy.orm.query.Query.first')
    @mock.patch('sqlalchemy.orm.session.Session.add')
    @mock.patch('core.model.parse_team_id')
    def test_import_file_calls_parse_players_if_squad_file(self, mock_parse_team_id, mock_add, mock_first, mock_count, mock_parse_players):
        """ Tests that parse_players is called if the HTML file is a Squad file """
        html_file = HTMLFile()
        html_file.type = PageTypes.Squad.value
        html_file.HTML = 'some HTML'

        mock_parse_players.return_value = []
        mock_parse_team_id.return_value = 3000

        team = Team()
        mock_first.result = team

        self.model.import_file(html_file)
        mock_parse_players.assert_called_with(html_file.HTML)

    @mock.patch('core.model.parse_pavilion')
    @mock.patch('sqlalchemy.orm.query.Query.first')
    @mock.patch('core.model.parse_team_id')
    @mock.patch('core.PyBatBase.Team.add_ranking')
    def test_import_file_calls_parse_pavilion_if_pavilion_file(self, mock_ranking,mock_parse_team_id, mock_first, mock_parse_pavilion):
        html_file = HTMLFile()
        html_file.type = PageTypes.Pavilion.value
        html_file.HTML = 'some HTML'
        

        mock_parse_pavilion.return_value = []
        mock_parse_team_id.return_value = 3000

        team = Team()
        team.rankings.append = mock.Mock()

        mock_first.result = team
        self.model.import_file(html_file)

        assert mock_parse_team_id.called

    @mock.patch('core.model.parse_team_id')
    @mock.patch('sqlalchemy.orm.session.Session.query')
    @mock.patch('sqlalchemy.orm.session.Session.add')
    def test_import_file_retrieves_team_from_file(self, mock_add, mock_query, mock_parse_team_id):

        test_id = 49800

        team = Team()

        html_file = HTMLFile()
        html_file.HTML = 'Some HTML'

        mock_query.return_value.filter_by = mock.Mock()

        mock_parse_team_id.return_value = test_id
        mock_result = mock.Mock(spec=Query)
        mock_result.count = mock.Mock()
        mock_result.count.return_value = 1

        mock_query.return_value.filter_by.return_value = mock_result

        self.model.import_file(html_file)

        mock_query.assert_called_with(Team)
        assert mock_parse_team_id.called
        mock_query.return_value.filter_by.assert_called_with(id=test_id)

    @mock.patch('sqlalchemy.orm.session.Session.query')
    def test_has_teams_returns_false_if_no_teams(self, mock_query):

        mock_query.return_value.count.return_value = 0

        result = self.model.has_teams()

        assert_false(result)

    @mock.patch('sqlalchemy.orm.session.Session.query')
    def test_has_teams_returns_true_if_teams(self, mock_query):

        mock_query.return_value.count.return_value = 1

        result = self.model.has_teams()

        assert_true(result)
