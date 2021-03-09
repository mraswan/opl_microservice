from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restplus import Api
from flask_login import LoginManager
import logging
import urllib
from oauthlib.oauth2 import WebApplicationClient
import os
from .oplapi.util.MultiProcessingLog import MultiProcessingLogHandler

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
            # configure the application
            self.__configure_app()
            # configure multiprocessing logging
            self.__configure_logging()
            #create Login Manager of the application
            self.__create_login_manager()
            #create OAuth Client of the application
            self.__create_oauth2_client()
            # Register the oplAPIBlueprint
            self.__register_blueprint_create_api()
            # all routes built, lets print them
            self.__list_routes()
            logger.info("*** Setup Complete ***")
            # ~~~~~~ START THE APP HERE ~~~~~~~#

        # User session management setup
        # https://flask-login.readthedocs.io/en/latest
        def __create_login_manager(self):
            self.login_manager = LoginManager()
            self.login_manager.init_app(self.oplAPIApp)
            logger.info("Login Manager Created!!!")

        def __create_oauth2_client(self):
            # OAuth 2 client setup
            self.oauth2_client = WebApplicationClient(self.oplAPIApp.config['OPL_GOOGLE_CLIENT_ID'])
            logger.info("OAuth2 Client Created!!!")

        def setup_controllers(self):
            from opl.oplapi.controller import oplController
            ## Setup all controller(s) here ###
            logger.info("All Controllers Setup!!!")

        def get_login_manager(self):
            return self.login_manager

        def get_oauth2_client(self):
            return self.oauth2_client

        def get_app(self):
            return self.oplAPIApp

        def get_api(self):
            return self.oplApi

        def __create_app(self):
            # oplAPIApp is the main application
            self.oplAPIApp = Flask(__name__)
            # cors = CORS(self.oplAPIApp, resources={r"/opl/*": {"origins": "*"}})
            self.oplAPIApp.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

        def __register_blueprint_create_api(self):
            logger.info ("Creating and registering Blueprints in oplAPIApp")
            # from opl.oplapi import oplAPIBlueprint
            logger.info("OPL Blueprint Created")
            oplAPIBlueprint = Blueprint('opl', __name__, url_prefix='/opl')
            self.oplApi = Api(oplAPIBlueprint, doc='/doc/', version='1.0', title='OPL APIs',
                         description='The Online Peer Learning API Service', )
            self.oplAPIApp.register_blueprint(oplAPIBlueprint)
            logger.info ("Blueprints registration complete")

        def __configure_app(self):
            # -------------- All Configurations Here --------------#
            # Load the default configuration in the application object
            try:
                configName = 'config.default'
                self.oplAPIApp.config.from_object(configName)
                logger.info (configName+' as object read successfully')
            except:
                logger.info ("problem reading "+configName+" as object. But moving on ...")

            # Load the configuration from the instance folder this is not to be checked in to git
            # add following line (with #) to your .git/info/exclude file instance
            try:
                local_config = '../instance/config.py'
                self.oplAPIApp.config.from_pyfile(local_config)
                logger.info ('"{}" as pyfile read successfully'.format(local_config))
            except:
                logger.info ('problem reading "{}" as pyfile. But moving on ...'.format(local_config))

            # Load the file specified by the APP_CONFIG_FILE environment variable
            # Variables defined here will override those in the default configuration
            # Make your start.sh like this:
            ###### APP_CONFIG_FILE=/var/www/yourapp/config/production.py
            ###### python run.py
            try:
                self.oplAPIApp.config.from_envvar('APP_CONFIG_FILE')
                logger.info ('APP_CONFIG_FILE envvar read successfully')
            except:
                logger.info ("problem reading APP_CONFIG_FILE envvar. But moving on ...")
            # -------------- All Configurations Here --------------#
            logger.info ("Read configurations in oplAPIApp")

        def __configure_logging(self):
            logFile = "{}/{}".format(self.oplAPIApp.config['LOG_DIR'] , self.oplAPIApp.config['LOG_FILE'])
            file_handler = MultiProcessingLogHandler(logFile, mode='a',
                                              maxBytes=self.oplAPIApp.config['LOG_FILE_SIZE'],
                                              backupCount=self.oplAPIApp.config['LOG_BACKUP_COUNT'],
                                              max_workers=self.oplAPIApp.config['LOG_THREAD_POOL'])
            console_handler = logging.StreamHandler()
            handler_list = self.oplAPIApp.logger.handlers[:]
            for log_handler in handler_list:
                logger.info("Removing log_handler:::::", log_handler)
                self.oplAPIApp.logger.removeHandler(log_handler)
            if self.oplAPIApp.debug:
                logger.info ("*************** Application DEBUG = True *********************")
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(
                    Formatter('%(asctime)s [%(levelname)s]: %(message)s [in %(pathname)s:%(lineno)d]'))
                console_handler.setLevel(logging.DEBUG)
                console_handler.setFormatter(Formatter('%(asctime)s [%(levelname)s]: %(message)s'))
                self.oplAPIApp.logger.addHandler(file_handler)
                self.oplAPIApp.logger.addHandler(console_handler)
                self.oplAPIApp.logger.setLevel(logging.DEBUG)
            else:
                logger.info("*************** Application DEBUG = False *********************")
                file_handler.setLevel(logging.ERROR)
                file_handler.setFormatter(
                    Formatter('%(asctime)s [%(levelname)s]: %(message)s [in %(pathname)s:%(lineno)d]'))
                self.oplAPIApp.logger.addHandler(file_handler)
                self.oplAPIApp.logger.setLevel(logging.INFO)


        def __list_routes(self):
            output = []
            for rule in self.oplAPIApp.url_map.iter_rules():
                methods = ','.join(rule.methods)
                line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
                output.append(line)
            logger.info ("All routes registered:")
            logger.info ("~~~~~~~~~~~~~~~~~~~~~")
            for line in sorted(output):
                logger.info(line)
            logger.info ("~~~~~~~~~~~~~~~~~~~~~")

        def run(self, ssl_context=None):
            logger.info('******************* Run Application *******************')
            self.oplAPIApp.run(use_debugger=True, debug=True, use_reloader=True,
                                port=self.oplAPIApp.config['SERVICE_PORT']
                                ,ssl_context=ssl_context) # run on https

    instance = None
    def __init__(self):
        if OplMain.instance is None:
            OplMain.instance = OplMain.__OnlyOne()
        else:
            pass

    def __getattr__(self, name):
        return getattr(self.instance, name)