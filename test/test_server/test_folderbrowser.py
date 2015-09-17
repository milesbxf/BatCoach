from server.servercore import FolderBrowser
import unittest.mock as mock
from nose.tools import assert_list_equal, raises, assert_equal

import cherrypy
from unittest.case import TestCase
from unittest.mock import patch


class TestFolderBrowser(TestCase):

    def cleanUp(self):
        for patcher in self.patchers:
            patcher.stop()

    def setUp(self):
        patch_listdir = patch('os.listdir')
        patch_isdir = patch('os.path.isdir')

        self.patchers = [patch_listdir, patch_isdir]
        self.addCleanup(self.cleanUp)

        self.mock_listdir = patch_listdir.start()
        self.mock_isdir = patch_isdir.start()

        self.folderBrowser = FolderBrowser()

        self.mock_listdir.return_value = ['folder1', 'file', 'folder3']

        self.mock_isdir.side_effect = [True, False, True]

        cherrypy.request.json = {'path': '/testpath/', 'subdir': 'testdir'}

    def test_list_only_gets_folders(self):
        result = self.folderBrowser.list()
        assert_list_equal(result['folders'], ['folder1', 'folder3'])

    def test_gives_newdir_in_response_object(self):
        result = self.folderBrowser.list()
        assert_equal(result['newdir'], '/testpath/testdir')

    @raises(cherrypy.HTTPError)
    def test_list_responds_HTTP400_if_invalid_folder(self):

        self.mock_listdir.side_effect = FileNotFoundError(
            'Wrong exception thrown! Should be HTTP400 error')

        self.folderBrowser.list()

    @mock.patch('os.path.join')
    def test_list_joins_path_and_subdir(self, mock_join):

        mock_join.return_value = 'joinedpath'

        self.folderBrowser.list()

        self.mock_listdir.assert_called_once_with('joinedpath')

    def test_gets_parent_with_dotdot(self):

        cherrypy.request.json = {'path': '/parent/child', 'subdir': '..'}

        result = self.folderBrowser.list()
        
        assert_equal(result['newdir'], '/parent')
