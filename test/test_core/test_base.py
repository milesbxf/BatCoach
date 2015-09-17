"""
Tests the PyBatBase database classes.
"""

from core.PyBatBase import HTMLFile, PageTypes, PageParseException
from unittest.case import TestCase
from unittest.mock import patch, Mock
from datetime import datetime
from time import mktime
from nose.tools import assert_is, raises, assert_equal


class TestHTMLFile(TestCase):
    """
    Tests instantiation of HTMLFile through the factory methods.
    """

    def cleanUp(self):
        """ Stops all unittest.mock patch objects """
        for patcher in self.patchers:
            patcher.stop()

    def setUp(self):
        """ Sets up tests and starts mock patchers """

        # patch open(file) and os.path.getmtime(file)
        patcher_open = patch('builtins.open')
        patcher_mtime = patch('os.path.getmtime')
        self.patchers = [patcher_open, patcher_mtime]
        self.addCleanup(self.cleanUp)

        self.mock_open = patcher_open.start()
        self.mock_open.return_value.__enter__ = lambda s: s
        self.mock_open.return_value.__exit__ = Mock()
        # return a fake HTML file
        self.mock_open.return_value.read.return_value = '<html><title>Battrick - Squad</title></html>'

        # fake modified time
        self.mock_mtime = patcher_mtime.start()
        self.test_date = datetime(2015, 1, 1, 12, 0, 10)
        self.mock_mtime.return_value = mktime(
            self.test_date.timetuple()) + 1e-6 * self.test_date.microsecond

    def test_HTMLFile_is_squad_page_when_parsing_squad_HTML(self):
        """ Tests that a squad.html page is correctly recognised as a squad file"""

        # return a fake HTML Squad file
        self.mock_open.return_value.read.return_value = '<html><title>Battrick - Squad</title></html>'
        htmlFile = HTMLFile.from_file('a_file')

        assert_is(htmlFile.type, PageTypes.Squad.value)

    @raises(PageParseException)
    def test_HTMLFile_inits_throws_PageParseException_if_page_not_recognised(self):
        """ Tests that a PageParseException is raised if an incorrect page is parsed """

        self.mock_open.return_value.read.return_value = '<html><title>Battrick - WrongPage</title></html>'
        HTMLFile.from_file('a_file')

    @raises(PageParseException)
    def test_HTMLFile_throws_PageParseException_if_empty_title(self):
        """ Tests that a PageParseException is raised if no <title> exists """

        self.mock_open.return_value.read.return_value = '<html></html>'
        HTMLFile.from_file('a_file')

    @raises(PageParseException)
    def test_HTMLFile_throws_PageParseException_if_wrong_title(self):
        """ Tests that a PageParseException is raised if the title is wrong """

        self.mock_open.return_value.read.return_value = '<html><head><title>WrongTitle</title></head></html>'
        HTMLFile.from_file('a_file')

    def test_HTMLfile_from_file_adds_modified_time(self):
        """ Tests that the file modified time is added to the object """

        htmlFile = HTMLFile.from_file('a_file')
        assert_equal(htmlFile.date_modified, self.test_date)

    def test_readfile_adds_imported_time(self):
        """ Tests that the 'current' time is added to the object """

        test_date = datetime(2010, 10, 8, 12, 50, 33)

        with patch('core.PyBatBase.datetime') as mock_date:
            # fake today's date
            mock_date.today.return_value = test_date

            htmlFile = HTMLFile.from_file('a_file')
            assert_equal(htmlFile.date_imported, test_date)
