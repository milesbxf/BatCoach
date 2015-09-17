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
from core.PyBatBase import HTMLFile
from datetime import datetime


class Config(object):
    """
    The Config service (at /api/config/) allows the front end to check
    whether a database has been initialised.
    """

    def __init__(self, model):
        self.model = model

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def dbinit(self):
        """   Checks whether any teams are in the database.   """
        return {'dbInit': self.model.has_teams()}


class Players(object):
    
    def __init__(self,model):
        self.model = model
    
    """
    The Players service (at /api/players/) provides access to the squad of
    players in the database.
    """
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        """
        Index (accessed at /api/players/). Currently a stub.
        """
        
        return model.get_players()
        
        # TODO implement Players.index
#         return [
#             {
#                 'firstName': 'John',
#                 'surName': 'Smith',
#                 'age': 18,
#                 'BTR': 3000,
#                 'wage': 812,
#                 'batAggression': '4',
#                 'batHand': 'R',
#                 'bowlAggression': '3',
#                 'bowlHand': 'R',
#                 'bowlType': 'M',
#                 'batForm': 9,
#                 'bowlForm': 7,
#                 'stamina': 3,
#                 'keeping': 4,
#                 'batting': 6,
#                 'concentration': 4,
#                 'bowling': 7,
#                 'consistency': 6,
#                 'fielding': 4}
#         ] * 10


class Import(object):
    """
    Import service, at /api/import/. The client can specify
    a list of files to import to the BatCoach backend.
    """

    def __init__(self, model):
        """
        Initialises the Import service, setting the default import directory to
         the user's home directory.
        """
        # load the user's home directory by default
        # TODO: check this works on Windows?
        self.import_dir = os.path.expanduser('~/')
        self.model = model
        self.date_format = "%Y-%m-%dT%H:%M:%S"

    def __check_import_dir__(self):
        """
        check the import directory actually exists;
        if not, throw a 500 HTTP code. Called by several subservices
        """
        if not os.path.exists(self.import_dir):
            raise cherrypy.HTTPError(
                500, 'Import directory ' +
                self.import_dir +
                ' is not valid'
            )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def dirname(self):
        """
        Returns the currently set import directory,
        which will be an absolute path. If the directory is
        not valid or does not exist, a HTTP 500 status is given.
        Returns a JSON string with {curDir: <directory>}.
        """
        self.__check_import_dir__()
        return {'curDir': self.import_dir}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def listfiles(self):
        """
        Lists the HTML files in the currently set import directory.
        If directory is not valid or does not exist, a HTTP 500 status
        is given. Returns a JSON object with {files: [list of files]}
        """
        self.__check_import_dir__()

        # get all HTML files in the import directory
        files = glob.glob(self.import_dir + "*.html")
        return {'files': files}

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def importfiles(self):
        """
        Imports the files provided as a list of local filenames in the request.
        """
        files = (cherrypy.request.json['files'])

        for filename in files:
            # generate HTMLFile objects from the filenames
            self.model.import_file(HTMLFile.from_file(filename))

        # TODO: add response with import success/failure
        return "true"

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
        """
        Changes the import directory to that given in the JSON request
        {newdir: <directory>}. It checks whether the path exists and returns a
        HTTP 400 error if not.
        """
        folder = cherrypy.request.json['newdir']

        # clean the given directory name in case it is URI encoded
        folder = unquote(folder)

        # ensure all paths end with a path separator to maintain consistency
        if not folder.endswith(os.pathsep):
            folder += os.pathsep

        if not os.path.exists(folder):
            raise cherrypy.HTTPError(
                400, 'Selected folder %s does not exist' % folder)

        self.import_dir = folder

    @cherrypy.expose
    def upload(self, file, data):
        """
        Directly upload a HTML file.
        """
        file_contents = file.file.read()

        timestamp = datetime.strptime(data[:data.index('.')], self.date_format)

        print(timestamp)
        
        self.model.import_file(
            HTMLFile.from_memory(file_contents, timestamp))

        return


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
        given doesn't exist, a HTTP 400 status is given. The JSON request
        should be in the form {path: <full path>, subdir: <new subdirectory>}.
        'subdir' is optional; if given, the path and subdir will be concatenated.
        """
        req = cherrypy.request.json
        newdir = ''

        # check that params are given
        if('path' not in req):
            raise cherrypy.HTTPError(400, "Directory not given")

        # three possibilities:
        #    only path given, newdir = path
        #    path + subdir given, newdir = path + subdir
        #    subdir is .., newdir = parent of path

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

            # sort by name
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
    cherrypy.tree.mount(Players(model), '/api/players')

    Import = Import(model)

    cherrypy.tree.mount(Import, '/api/import')

    Config = Config(model)

    cherrypy.tree.mount(Config, '/api/config')

    cherrypy.tree.mount(FolderBrowser(), '/api/folders')
    cherrypy.engine.start()
    cherrypy.engine.block()
