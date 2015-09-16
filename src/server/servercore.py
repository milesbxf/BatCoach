"""
==========
servercore
==========

Contains the REST backend services serving at /api/ and starts the server.

The web services provide a REST interface to the BatCoach backend logic.
All information that the frontend needs can be accessed through various URLs.
"""
import cherrypy
import os
import glob
from core.model import Model
from urllib.parse import unquote


class Config(object):

    def __init__(self, model):
        self.model = model

    @cherrypy.expose
    def checkdbinit(self):
        return {'db_initialised': self.model.has_teams()}


class Players(object):
    """
    The Players service (at /api/players/) provides the squad.
    """
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        """
        Index (accessed at /api/players/). Currently a stub.
        """
        # TODO implement Players.index
        return [
            {
                'firstName': 'John',
                'surName': 'Smith',
                'age': 18,
                'BTR': 3000,
                'wage': 812,
                'batAggression': '4',
                'batHand': 'R',
                'bowlAggression': '3',
                'bowlHand': 'R',
                'bowlType': 'M',
                'batForm': 9,
                'bowlForm': 7,
                'stamina': 3,
                'keeping': 4,
                'batting': 6,
                'concentration': 4,
                'bowling': 7,
                'consistency': 6,
                'fielding': 4}
        ] * 10


class Import(object):
    """
    Import service, at /api/import/. The client can specify
    a list of files to import to the BatCoach backend.
    """

    def __init__(self, model):
        # load the user's home directory by default
        self.import_dir = os.path.expanduser('~/')
        self.model = model

    def __check_import_dir__(self):
        """
        check the import directory actually exists;
        if not, throw a 500 HTTP code. Called by several subservices
        """
        if not os.path.exists(self.import_dir):
            raise cherrypy.HTTPError(
                500, 'Import directory ' +
                self.import_dir +
                ' is not valid')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def dirname(self):
        """
        Returns the currently set import directory,
        which will be an absolute path. If the directory is
        not valid or does not exist, a HTTP 500 status is given.
        """
        self.__check_import_dir__()
        return {'curDir': self.import_dir}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def listfiles(self):
        """
        Lists the HTML files in the currently set import directory.
        If directory is not valid or does not exist, a HTTP 500 status
        is given.
        """
        self.__check_import_dir__()
        files = glob.glob(self.import_dir + "*.html")
        return {'files': files}

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def importfiles(self):
        """ Imports the files provided as a list in the request. """
        files = (cherrypy.request.json)

        output = self.model.import_multiple_files(files['files'])

        return output

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def newfiles(self):
        """
        Checks if files are available in the import folder.
        Throws HTTP 500 if import directory is no longer valid.
        """
        self.__check_import_dir__()
        files = glob.glob(self.import_dir + "*.html")
        return len(files) > 0

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def changedir(self):
        folder = cherrypy.request.json['newdir']
        folder = unquote(folder)

        if(not folder.endswith('/')):
            folder += '/'

        if(not os.path.exists(folder)):
            raise cherrypy.HTTPError(
                400, 'Selected folder %s does not exist' % folder)

        self.import_dir = folder


class FolderBrowser(object):
    """
    The FolderBrowser service, at /api/folders/,
    is a simple service for browsing folders on the local
    file system.
    """
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def list(self):
        """
        Lists the folders in the given directory. If the directory
        given doesn't exist, a HTTP 400 status is given.
        """
        req = cherrypy.request.json
        print(req)
        newdir = ''
        path = ''
        if('path' not in req):
            raise cherrypy.HTTPError(400, "Directory not given")
        elif 'subdir' in req:
            if(req['subdir'] == '..'):
                # get parent directory
                newdir = os.path.abspath(os.path.join(req['path'], os.pardir))
            else:
                newdir = os.path.join(req['path'], req['subdir'])
        else:
            newdir = req['path']
        try:
            # get all subdirectories
            folders = [o for o in os.listdir(newdir)
                       if os.path.isdir(os.path.join(newdir, o))]
            folders = sorted(folders)
        except FileNotFoundError:
            raise cherrypy.HTTPError(
                400, 'Folder ' + newdir + 'does not exist')

        return {'folders': folders, 'newdir': newdir}

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    model = Model(dbcon="sqlite:///db.db", echo=True)

    cherrypy.config.update("server.conf")
    cherrypy.tree.mount(None, '/', "server.conf")
    cherrypy.tree.mount(Players(), '/api/players')

    Import = Import(model)

    cherrypy.tree.mount(Import, '/api/import')

    Config = Config(model)

    cherrypy.tree.mount(Config, '/api/config')

    cherrypy.tree.mount(FolderBrowser(), '/api/folders')
    cherrypy.engine.start()
    cherrypy.engine.block()
