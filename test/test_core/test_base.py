from core.PyBatBase import HTMLFile, PageTypes, PageParseException
from unittest.case import TestCase
from unittest.mock import patch, Mock
from datetime import datetime
from time import mktime
from nose.tools import assert_is, raises, assert_equal


class TestHTMLFile(TestCase):

    def cleanUp(self):
        for patcher in self.patchers:
            patcher.stop()

    def setUp(self):

        patcher_open = patch('builtins.open')
        patcher_mtime = patch('os.path.getmtime')
        self.patchers = [patcher_open, patcher_mtime]
        self.addCleanup(self.cleanUp)
        self.mock_open = patcher_open.start()
        self.mock_open.return_value.__enter__ = lambda s: s
        self.mock_open.return_value.__exit__ = Mock()
        self.mock_open.return_value.read.return_value = '<html><title>Battrick - Squad</title></html>'

        self.mock_mtime = patcher_mtime.start()
        self.test_date = datetime(2015, 1, 1, 12, 0, 10)

        self.mock_mtime.return_value = mktime(
            self.test_date.timetuple()) + 1e-6 * self.test_date.microsecond

    def test_HTMLFile_inits_pagetype_from_filename(self):

        self.mock_open.return_value.read.return_value = '<html><title>Battrick - Squad</title></html>'

        htmlFile = HTMLFile.from_file('a_file')

        assert_is(htmlFile.type, PageTypes.Squad.value)

    @raises(PageParseException)
    def test_HTMLFile_inits_throws_PageParseException_if_page_not_recognised(self):
        self.mock_open.return_value.read.return_value = '<html><title>Battrick - WrongPage</title></html>'

        htmlFile = HTMLFile.from_file('a_file')

    @raises(PageParseException)
    def test_HTMLFile_throws_PageParseException_if_empty_title(self):
        self.mock_open.return_value.read.return_value = '<html></html>'

        htmlFile = HTMLFile.from_file('a_file')

    @raises(PageParseException)
    def test_HTMLFile_throws_PageParseException_if_wrong_title(self):
        self.mock_open.return_value.read.return_value = '<html><head><title>WrongTitle</title></head></html>'

        htmlFile = HTMLFile.from_file('a_file')

    def test_HTMLfile_adds_modified_time(self):
        htmlFile = HTMLFile.from_file('a_file')

        assert_equal(htmlFile.date_modified, self.test_date)

    def test_readfile_adds_imported_time(self):

        test_date = datetime(2010, 10, 8, 12, 50, 33)

        with patch('core.PyBatBase.datetime') as mock_date:
            mock_date.today.return_value = test_date

            htmlFile = HTMLFile.from_file('a_file')
            assert_equal(htmlFile.date_imported, test_date)
