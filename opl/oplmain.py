from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restplus import Api
import logging
import urllib

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OplMain():
    '''
    Internal class
    '''
    class __OnlyOne:
        def __init__(self):
            # ~~~~~~ START THE APP HERE ~~~~~~~#
            logger.info('*** Setting up Application ***')
            #create app
            self.__create_app()
            #configure the application
            self.__configure_app()
            # Register the oplAPIBlueprint
            self.__register_blueprint_create_api()
            # all routes built, lets print them
            self.__list_routes()
            print("*** Setup Complete ***")
            # ~~~~~~ START THE APP HERE ~~~~~~~#

        def setup_controllers(self):
            from opl.oplapi.controller import oplController
            print("All Controllers Setup!!!")

        def get_app(self):
            return self.oplAPIApp

        def get_api(self):
            return self.oplApi

        def __create_app(self):
            # oplAPIApp is the main application
            self.oplAPIApp = Flask(__name__)
            cors = CORS(self.oplAPIApp, resources={r"/opl/*": {"origins": "*"}})

        def __register_blueprint_create_api(self):
            print ("Creating and registering Blueprints in oplAPIApp")
            # from opl.oplapi import oplAPIBlueprint
            print("OPL Blueprint Created")
            oplAPIBlueprint = Blueprint('opl', __name__, url_prefix='/opl')
            self.oplApi = Api(oplAPIBlueprint, doc='/doc/', version='1.0', title='OPL APIs',
                         description='The Online Peer Learning API Service', )
            self.oplAPIApp.register_blueprint(oplAPIBlueprint)
            print ("Blueprints registration complete")

        def __configure_app(self):
            # -------------- All Configurations Here --------------#
            # Load the default configuration in the application object
            try:
                configName = 'config.default'
                self.oplAPIApp.config.from_object(configName)
                print (configName+' as object read successfully')
            except:
                print ("problem reading "+configName+" as object. But moving on ...")

            # Load the configuration from the instance folder this is not to be checked in to git
            # add following line (with #) to your .git/info/exclude file instance
            try:
                self.oplAPIApp.config.from_pyfile('../instance/config.py')
                print ('"../instance/config.py" as pyfile read successfully')
            except:
                print ('problem reading "../instance/config.py" as pyfile. But moving on ...')

            # Load the file specified by the APP_CONFIG_FILE environment variable
            # Variables defined here will override those in the default configuration
            # Make your start.sh like this:
            ###### APP_CONFIG_FILE=/var/www/yourapp/config/production.py
            ###### python run.py
            try:
                self.oplAPIApp.config.from_envvar('APP_CONFIG_FILE')
                print ('APP_CONFIG_FILE envvar read successfully')
            except:
                print ("problem reading APP_CONFIG_FILE envvar. But moving on ...")
            # -------------- All Configurations Here --------------#
            print ("Read configurations in oplAPIApp")

        def __list_routes(self):
            output = []
            for rule in self.oplAPIApp.url_map.iter_rules():
                methods = ','.join(rule.methods)
                line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
                output.append(line)
            print ("All routes registered:")
            print ("~~~~~~~~~~~~~~~~~~~~~")
            for line in sorted(output):
                print(line)
            print ("~~~~~~~~~~~~~~~~~~~~~")

        def run(self):
            logger.info('******************* Run Application *******************')
            self.oplAPIApp.run(use_debugger=True, debug=True, use_reloader=True,
                                port=self.oplAPIApp.config['SERVICE_PORT'])
                                # ,ssl_context='adhoc') # run on https

    instance = None
    def __init__(self):
        if OplMain.instance is None:
            OplMain.instance = OplMain.__OnlyOne()
        else:
            pass

    def __getattr__(self, name):
        return getattr(self.instance, name)



    # def
# Define the blueprint: 'oplapi', set its url prefix: app.url/oplapi
# print ("OPL Blueprint Created")
# oplAPIBlueprint = Blueprint('opl', __name__, url_prefix='/opl')
# oplApi = Api(oplAPIBlueprint, doc='/doc/', version='1.0', title='OPL APIs', description='The Online Peer Learning API Service', )


# from opl.oplapi.controller import statusController
# from opl.oplapi.controller import oplController
# from opl.oplapi.controller import matchingCSVController
# from opl.oplapi.controller import findCandidatesJobsController
# from opl.oplapi.controller import assistantController
