from flask import Blueprint, send_from_directory, request
import logging
from ..service.assistService import AssistService
import sys
import json
from flask_restplus import Api, Resource, fields, reqparse

from rfy.rfyapi import rfyApi

sugg = rfyApi.namespace('assistant', description='RFY Watson Assistant API')
print("namespace " + sugg.name + " is setup")

@sugg.route('/assist')
class AssistController(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('query', type=str, help='Query', required=True, location='args')
    '''Assist Payload'''

    @sugg.doc('assist_send')
    def post(self):
        '''Auto suggest a list of businesses based on input string'''
        # args = AssistController.parser.parse_args()
        service = AssistService()
        # print(args.get("query"))
        payLoad = None
        try:
            payLoad = rfyApi.payload["input"]
        except Exception as ex:
            print("Payload had exception: {0}, moving on ...".format(ex))

        results = service.assist(payLoad)
        # httpStatusCode = 200
        # if results.statusCode <> "S_OK":
        #     httpStatusCode = 404
        return results
        # , httpStatusCode