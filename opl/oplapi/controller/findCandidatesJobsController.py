from flask import Blueprint, send_from_directory, request
import logging
from ..service.findService import FindService
import sys
import json
from flask_restplus import Api, Resource, fields, reqparse

from opl.oplapi import oplApi

sugg = oplApi.namespace('match', description='RFI Candidates and Jobs API')
print("namespace " + sugg.name + " is setup")

candidateinfo = oplApi.model('CandidateInfo', {
    'id': fields.String(attribute='id', description='Candidate ID'),
    'name': fields.String(attribute='name', description='Candidate Name'),
    'designation': fields.String(attribute='designation', description='Designation Title'),
    'expsummary': fields.String(attribute='expsummary', description='Experience Summary'),
    'industry': fields.String(attribute='industry', description='Industry'),
    'country': fields.String(attribute='country', description='Country'),
    'matchscore': fields.Float(attribute='matchscore', description='Match Score')
})

matchedCandidates = oplApi.model('FindCandidatesResponse', {
    'recordCount': fields.Integer(attribute='recordCount', description='Record Count'),
    'candidateInfos': fields.List(fields.Nested(candidateinfo))
})

jobinfo = oplApi.model('JobInfo', {
    'id': fields.String(attribute='id', description='Job ID'),
    'title': fields.String(attribute='title', description='Title'),
    'description': fields.String(attribute='description', description='Description'),
    'url': fields.String(attribute='url', description='URL'),
    'matchscore': fields.Float(attribute='matchscore', description='Match Score'),
    'titlecategories': fields.String(attribute='title_categories', description='Title Categories'),
    'descriptioncategories': fields.String(attribute='description_categories', description='Description Categories')
})

matchedJobs = oplApi.model('FindJobsResponse', {
    'recordCount': fields.Integer(attribute='recordCount', description='Record Count'),
    'jobInfos': fields.List(fields.Nested(jobinfo))
})


@sugg.route('/enrichedcandidates')
class EnrichedCandidatesController(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('designation', type=str, help='Designation', required=True, location='args')
    parser.add_argument('designationcategories', type=str, help='Designation Categories', required=False, location='args')
    parser.add_argument('expsummarycetegories', type=str, help='Exp Summary cetegories', required=False, location='args')
    '''Matching Enriched Candidate Profiles to a Job'''

    @sugg.doc('list_enrichedcandidates')
    @sugg.expect(parser, validate=True)
    @sugg.marshal_with(matchedCandidates)
    def get(self):
        '''Auto suggest a list of businesses based on input string'''
        args = EnrichedCandidatesController.parser.parse_args()
        service = FindService()
        print(args.get("designation"))
        print(args.get("designationcategories"))
        print(args.get("expsummarycetegories"))
        results = service.matchEnrichedCandidates(args.get("designation"),
                                                  "" if (args.get("designationcategories") == None) else args.get("designationcategories"),
                                                  "" if (args.get("expsummarycetegories") == None) else args.get("expsummarycetegories"))
        # httpStatusCode = 200
        # if results.statusCode <> "S_OK":
        #     httpStatusCode = 404
        return results

@sugg.route('/candidates')
class CandidatesController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('jobtitle', type=str, help='Job Title', required=True, location='args')
    '''Matching Candidates to a Job'''

    @sugg.doc('list_candidates')
    @sugg.expect(parser, validate=True)
    @sugg.marshal_with(matchedCandidates)
    def get(self):
        '''Auto suggest a list of businesses based on input string'''
        args = CandidatesController.parser.parse_args()
        service = FindService()
        print(args.get("jobtitle"))
        results = service.matchCandidates(args.get("jobtitle"))
        # httpStatusCode = 200
        # if results.statusCode <> "S_OK":
        #     httpStatusCode = 404
        return results
        # , httpStatusCode


@sugg.route('/jobs')
class JobsController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('query', type=str, help='Query', required=True, location='args')
    '''Matching Jobs to a Query'''

    @sugg.doc('list_jobs')
    @sugg.expect(parser, validate=True)
    @sugg.marshal_with(matchedJobs)
    def get(self):
        '''Auto suggest a list of businesses based on input string'''
        args = JobsController.parser.parse_args()
        service = FindService()
        print(args.get("query"))
        results = service.matchJobs(args.get("query"))
        # httpStatusCode = 200
        # if results.statusCode <> "S_OK":
        #     httpStatusCode = 404
        return results
        # , httpStatusCode