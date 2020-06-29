from . import oplmain
from flask import redirect, make_response
import json
from simplexml import dumps

# main object created here:
oplMain = oplmain.OplMain()
oplAPIApp = oplMain.get_app()
oplApi = oplMain.get_api()
# setup all controller here
oplMain.setup_controllers()

# redirect the root to swagger documentation
@oplAPIApp.route('/')
def home():
    return redirect('/opl/doc/', code=302)

@oplApi.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp

@oplApi.representation('application/xml')
def output_xml(data, code, headers=None):
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(dumps({'response': data}), code)
    resp.headers.extend(headers or {})
    return resp

# run app if this is starting point
if __name__ == '__main__':
    oplMain.run()


# from flask import Flask, Blueprint, url_for, redirect
# import logging
# #from werkzeug.contrib.fixers import ProxyFix
# #from flask_restplus import Api, Resource, fields
# from flask_cors import CORS, cross_origin
#
# def main():
#     #configure the application
#     configureApp()
#     # Register the oplAPIBlueprint
#     registerBlueprint()
#     # all routes built, lets print them
#     list_routes(oplAPIApp)
#
# def registerBlueprint():
#     print ("Creating and registering Blueprints in oplAPIApp")
#     from opl.oplapi import oplAPIBlueprint
#     oplAPIApp.register_blueprint(oplAPIBlueprint)
#     print ("Blueprints registration complete")
#
# def configureApp():
#     # -------------- All Configurations Here --------------#
#     # Load the default configuration in the application object
#     try:
#         configName = 'config.default'
#         oplAPIApp.config.from_object(configName)
#         print (configName+' as object read successfully')
#     except:
#         print ("problem reading "+configName+" as object. But moving on ...")
#
#     # Load the configuration from the instance folder this is not to be checked in to git
#     # add following line (with #) to your .git/info/exclude file instance
#     try:
#         oplAPIApp.config.from_pyfile('../instance/config.py')
#         print ('"../instance/config.py" as pyfile read successfully')
#     except:
#         print ('problem reading "../instance/config.py" as pyfile. But moving on ...')
#
#     # Load the file specified by the APP_CONFIG_FILE environment variable
#     # Variables defined here will override those in the default configuration
#     # Make your start.sh like this:
#     ###### APP_CONFIG_FILE=/var/www/yourapp/config/production.py
#     ###### python run.py
#     try:
#         oplAPIApp.config.from_envvar('APP_CONFIG_FILE')
#         print ('APP_CONFIG_FILE envvar read successfully')
#     except:
#         print ("problem reading APP_CONFIG_FILE envvar. But moving on ...")
#     # -------------- All Configurations Here --------------#
#     print ("Read configurations in oplAPIApp")
#
# def list_routes(app):
#     import urllib
#
#     output = []
#     for rule in app.url_map.iter_rules():
#         methods = ','.join(rule.methods)
#         line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
#         output.append(line)
#     print ("All routes registered:")
#     print ("~~~~~~~~~~~~~~~~~~~~~")
#     for line in sorted(output):
#         print(line)
#     print ("~~~~~~~~~~~~~~~~~~~~~")
#
#
# #~~~~~~ START THE APP HERE ~~~~~~~#
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.info('******************* Start Application *******************')
#
# # oplAPIApp is the main application
# oplAPIApp = Flask(__name__)
# cors = CORS(oplAPIApp, resources={r"/opl/*": {"origins": "*"}})
#
#
# print ("Created oplAPIApp app")
# # run the main function
# main()
# #~~~~~~ START THE APP HERE ~~~~~~~#
#
# # redirect the root to swagger documentation
# @oplAPIApp.route('/')
# def home():
#     return redirect('/opl/doc/', code=302)
#
# if __name__ == '__main__':
#     oplAPIApp.run(use_debugger=True, debug=True, use_reloader=True,
#                   port=oplAPIApp.config['SERVICE_PORT'])