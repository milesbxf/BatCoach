from server.servercore import Import
import unittest.mock as mock
import cherrypy
from nose.tools import raises, assert_true
from unittest.mock import patch, call
from unittest.case import TestCase
from core.model import Model
from core.PyBatBase import HTMLFile
from datetime import datetime


class ModelMock(Model):

    def __init__(self, dbcon='sqlite:///:memory:', echo=False):
        pass

    def import_multiple_files(self, files):
        pass

    def import_file(self, file):
        pass

    def __read_file__(self, file, commit_to_db=True):
        pass


class TestImport(TestCase):

    def setUp(self):
        patcher = patch('os.path.exists')
        self.addCleanup(patcher.stop)
        self.mock_exists = patcher.start()
        self.mock_exists.return_value = True
        self.mock_model = mock.Mock(spec=ModelMock)
        self.import_ctrl = Import(self.mock_model)
        self.import_ctrl.import_dir = 'testdir'

    def test_dirname_returns_dirname(self):
        assert self.import_ctrl.dirname()[
            'curDir'] == self.import_ctrl.import_dir

    @raises(cherrypy.HTTPError)
    def test_dirname_throws_HTTP_500_if_invalid_import_folder(self):
        self.mock_exists.return_value = False
        self.import_ctrl.dirname()

    @mock.patch('glob.glob')
    def test_newfiles_checks_if_files_exist(self, mock_glob):

        mock_glob.return_value = []
        result = self.import_ctrl.newfiles()
        mock_glob.assert_called_with(self.import_ctrl.import_dir + '*.html')

        assert result is False

        mock_glob.return_value = ['file.html', 'lol.html']
        result = self.import_ctrl.newfiles()
        mock_glob.assert_called_with(self.import_ctrl.import_dir + '*.html')

        assert result is True

    @raises(cherrypy.HTTPError)
    def test_newfiles_throws_HTTP_500_if_invalid_import_folder(self):
        self.mock_exists.return_value = False
        self.import_ctrl.newfiles()

    @mock.patch('glob.glob')
    def test_listfiles_gets_files_in_directory(self, mock_glob):
        mock_glob.return_value = []
        result = self.import_ctrl.listfiles()
        mock_glob.assert_called_with(self.import_ctrl.import_dir + '*.html')

        assert len(result['files']) == 0

        mock_glob.return_value = ['file.html', 'lol.html']
        result = self.import_ctrl.listfiles()
        mock_glob.assert_called_with(self.import_ctrl.import_dir + '*.html')

        assert len(result['files']) == 2

    @raises(cherrypy.HTTPError)
    def test_listfiles_throws_HTTP_500_if_invalid_import_folder(self):
        self.mock_exists.return_value = False
        self.import_ctrl.listfiles()

    @mock.patch('core.PyBatBase.HTMLFile.from_file')
    def test_import_files(self, mock_from_file):

        mock_from_file.return_value = HTMLFile()

        cherrypy.request.json = {
            'files': ['file1.html', 'file2.html', 'file3.html']}
        result = self.import_ctrl.importfiles()

        assert result

    @raises(cherrypy.HTTPError)
    @mock.patch('os.path.exists')
    def test_changedir_gives_HTTP400_if_directory_doesnt_exist(self, mock_exists):
        cherrypy.request.json = {'newdir': 'doesntexist'}
        mock_exists.return_value = False
        self.import_ctrl.changedir()

        assert mock_exists.called

    @mock.patch('core.PyBatBase.HTMLFile.from_memory')
    def test_uploads_and_formats_date(self, mock_from_memory):
        # tests the upload single file function with an unformatted date
        date = "2015-06-18T15:49:20.267Z"

        file = mock.Mock()

        self.import_ctrl.upload(file, date)

        actual_date = datetime.strptime(
            date[:date.index('.')], self.import_ctrl.date_format)

        print(actual_date)

        assert_true(actual_date == mock_from_memory.call_args_list[0][0][1])
