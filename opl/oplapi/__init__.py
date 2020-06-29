# import json
#
# from flask import Blueprint, make_response
# from flask_restplus import Api
# from simplexml import dumps
#
# # Define the blueprint: 'oplapi', set its url prefix: app.url/oplapi
# print ("OPL Blueprint Created")
# oplAPIBlueprint = Blueprint('opl', __name__, url_prefix='/opl')
# oplApi = Api(oplAPIBlueprint, doc='/doc/', version='1.0', title='OPL APIs', description='The Online Peer Learning API Service', )
#
# @oplApi.representation('application/json')
# def output_json(data, code, headers=None):
#     resp = make_response(json.dumps(data), code)
#     resp.headers.extend(headers or {})
#     return resp
#
# @oplApi.representation('application/xml')
# def output_xml(data, code, headers=None):
#     """Makes a Flask response with a XML encoded body"""
#     resp = make_response(dumps({'response': data}), code)
#     resp.headers.extend(headers or {})
#     return resp
#
#
# # from opl.oplapi.controller import statusController
# from opl.oplapi.controller import oplController
# # from opl.oplapi.controller import matchingCSVController
# # from opl.oplapi.controller import findCandidatesJobsController
# # from opl.oplapi.controller import assistantController
