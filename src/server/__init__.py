import cherrypy,os

current_dir = os.path.dirname(os.path.abspath(__file__))

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"


class Players(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return [
                {
                 'firstName':'John',
                 'surName':'Smith',
                 'age':18,
                 'BTR':3000,
                 'wage':812,
                 'batAggression':'4',
                 'batHand':'R',
                 'bowlAggression':'3',
                 'bowlHand':'R',
                 'bowlType':'M',
                 'batForm':9,
                 'bowlForm':7,
                 'stamina':3,
                 'keeping':4,
                 'batting':6,
                 'concentration':4,
                 'bowling':7,
                 'consistency':6,
                 'fielding':4}
                ] *10
                
class Import(object):
    @cherrypy.expose
    def dirname(self):
        return "/home/miles/batcoach/"                

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def listfiles(self):
        return ['pavilion.html','squad.html','etc.html']

    @cherrypy.tools.json_in()
    @cherrypy.expose
    def importfiles(self):
        files = (cherrypy.request.json)
        return "true"


if __name__ == '__main__':
    cherrypy.config.update("server.conf")
    cherrypy.tree.mount(None, '/',"server.conf" )
    cherrypy.tree.mount(HelloWorld(),'/hello')
    cherrypy.tree.mount(Players(),'/api/players')
    cherrypy.tree.mount(Import(),'/api/import')
    cherrypy.engine.start()
    cherrypy.engine.block()