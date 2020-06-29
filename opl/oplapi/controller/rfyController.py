import os.path
import sys
from flask_restplus import Resource, fields
from .. import rfyApi

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ..service.rfyMatchService import RfyMatchService
from ..service.filterUtlityService import FilterUtilityService

rfyns = rfyApi.namespace('rfy', description='RFY API Description Here')
print ("namespace " + rfyns.name + " is setup")


matchedcandidate = rfyApi.model('MatchedCandidate', {
    'statuscode': fields.String(attribute='statusCode', description='Status Code'),
    'job_id': fields.String(attribute='job_id', description='Job Id'),
    'job_title': fields.String(attribute='job_title', description='Job title'),
    'job_description': fields.String(attribute='job_description', description='Job description'),
    'distance': fields.String(attribute='distance', description='Distance between Candidate & Job location'),
    'seniority_level': fields.String(attribute='seniority_level', description='Difference between Candidate and Job Seniority Level'),
    'solr_score': fields.String(attribute='solr_score', description='Raw Solr Score')
})


matchedjobs = rfyApi.model('MatchedJobs', {
    'statuscode': fields.String(attribute='statusCode', description='Status Code'),
    'cand_id': fields.String(attribute='cand_id', description='connetion Id'),
    'cand_title': fields.String(attribute='cand_title', description='Connection title or Designation'),
    'cand_description': fields.String(attribute='cand_description', description='Connection description'),
    'distance': fields.String(attribute='distance', description='Distance between Connection & Job location'),
    'seniority_level': fields.String(attribute='seniority_level', description='Difference between Connection and Job Seniority Level'),
    'solr_score': fields.String(attribute='solr_score', description='Raw Solr Score')
})

baseResponse = rfyApi.model('BaseResponse', {

})



'''Shows a list of all Jobs that match this candidates'''
@rfyns.route('/matchedjobs')
class SearchCandidate(Resource):

    parser = rfyns.parser()
    parser.add_argument('project', type=str, help='Specify Project as ACCENTURE, ACCENTURE_CRP, TALENT & IBM',
                        required=True, location='args')
    parser.add_argument('title', type=str, help='connection Title', required=True, location='args')
    parser.add_argument('description', type=str, help='connection Description', required=False, location='args')
    parser.add_argument('senioritylevel', type=str, help='connection Seniority Level', required=False, location='args')
    parser.add_argument('coordinates', type=str, help='connection Latitude & Longitude', required=True, location='args')
    parser.add_argument('country', type=str, help='connection Country', required=True, location='args')
    @rfyns.doc('list_Jobs')
    @rfyns.expect(parser, validate=True)
    @rfyns.marshal_with(matchedcandidate)
    def get(self):
        '''Get Matched Jobs'''                #Description of API shown on the swagger UI
        args = SearchCandidate.parser.parse_args()
        rfyMatchService = RfyMatchService()
        masterList = rfyMatchService.getJobMatchesForCandidate( args.get("project"), args.get("title"), args.get("description"), args.get("senioritylevel"),
                                                               args.get("coordinates"), args.get("country") )

        return masterList, 200, {'Content-Type': 'application/json; charset=utf8'}


@rfyns.route('/matchedcandidate')
class SearchJobs(Resource):
    parser = rfyns.parser()
    parser.add_argument('project', type=str, help='Specify Project as ACCENTURE, ACCENTURE_CRP, TALENT & IBM',
                        required=True, location='args')
    parser.add_argument('title', type=str, help='Job Title', required=True, location='args')
    parser.add_argument('description', type=str, help='Job Description', required=False, location='args')
    parser.add_argument('senioritylevel', type=str, help='Job Seniority Level', required=False, location='args')
    parser.add_argument('coordinates', type=str, help='Job Latitude & Longitude', required=True, location='args')
    parser.add_argument('country', type=str, help='Job Country', required=True, location='args')
    '''Shows a list of all Connections that match this Jobs'''

    @rfyns.doc('list_candidates')
    @rfyns.expect(parser, validate=True)
    @rfyns.marshal_with(matchedjobs)
    def get(self):
        '''Get Matched Candidate'''                     #Description of API shown on the swagger UI
        args = SearchJobs.parser.parse_args()
        rfyMatchService = RfyMatchService()
        masterList = rfyMatchService.getCandidateMatchesForJob(args.get("project"), args.get("title"), args.get("description"), args.get("senioritylevel"),
                                                               args.get("coordinates"), args.get("country"))

        return masterList, 200, {'Content-Type': 'application/json; charset=utf8'}



@rfyns.route('/dataimport')
class DataImport(Resource):
    parser = rfyns.parser()
    parser.add_argument('project', type=str, help='Specify Project as ACCENTURE, ACCENTURE_CRP, TALENT & IBM',
                        required=True, location='args')
    parser.add_argument('command', type=str, help='Command Parameter as full-import or delta-import', required=True, location='args')
    parser.add_argument('clean', type=str, help='Clean Parameter', required=True, location='args')
    parser.add_argument('entity', type=str, help='Entity Parameter', required=False, location='args')
    '''Importing data to Solr from MySql'''

    @rfyns.doc('list_data')
    @rfyns.expect(parser, validate=True)
    @rfyns.marshal_with(baseResponse)
    def get(self):
        '''Importing data to Solr from MySql'''                     #Description of API shown on the swagger UI
        args = DataImport.parser.parse_args()
        rfyMatchService = RfyMatchService()
        retObjRawData = rfyMatchService.importDataToSolr(args)
        retVal = retObjRawData
        return retVal
