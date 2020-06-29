import json
from ... import rfyAPIApp as app
from ..model.findServiceResponse import *
from watson_developer_cloud import DiscoveryV1

# from ..exception.APIError import APIError
# from watson_developer_cloud import WatsonApiException

import requests

class FindService:
    def __init__(self):
        print("FindCandidate Service Initialized")

    '''
    Replace a set of multiple sub strings with a new string in main string.
    '''
    def replaceMultiple(self, mainString, toBeReplaces, newString):
        # Iterate over the strings to be replaced
        for elem in toBeReplaces:
            # Check if string is in the main string
            if elem in mainString:
                # Replace the string
                mainString = mainString.replace(elem, newString)
        return mainString

    # Clease for Watson Discovery Query Language
    def cleanseDQL(self, inputstr):
        return self.replaceMultiple(inputstr,[',', ':', '|', '<','>','=','~','*','(',')','^','"'] , " ")

    # match through enriched fields
    def matchEnrichedCandidates(self, designation, designation_categories="", expsummary_cetegories=""):
        discovery_api_query_url = 'https://gateway-wdc.watsonplatform.net/discovery/api/v1/environments/'\
                                  + app.config['DISCOVERY_ENVIRONMENT_ID']\
                                  + '/collections/'\
                                  + app.config['DISCOVERY_CONNECTIONS_COLLECTION_ID']\
                                  + '/query'
        queryString =  "(DESIGNATION:"+self.cleanseDQL(designation)+"^2" + \
        "| EXPERIENCE_SUMMARY:"+self.cleanseDQL(designation)+")"
        if (designation_categories.strip() != ""):
            queryString = queryString + ",(((enriched_DESIGNATION.categories.label:" \
            + designation_categories+", enriched_DESIGNATION.categories.score > 0.60) "
            if (expsummary_cetegories.strip() != ""):
                queryString = queryString + "| (" \
                + "enriched_EXPERIENCE_SUMMARY.categories.label:" \
                + expsummary_cetegories+", enriched_EXPERIENCE_SUMMARY.categories.score  > 0.75)"
            queryString = queryString + "))"
            # +", (enriched_INDUSTRY.categories.label:" \
            # + designation_categories \
            # +", enriched_INDUSTRY.categories.score > 0.50)" \
            # + ")"

        reqParams = {"version" : app.config['DISCOVERY_API_VERSION'],
            'deduplicate' : 'false',
            'highlight' : 'false',
            # 'passages' : 'true',
            # 'passages.count' : '5',
            'query' : queryString}
        print (reqParams)
        resp = requests.get( discovery_api_query_url
                            , params=reqParams
                            , auth=('apikey', app.config['DISCOVERY_API_KEY'])
                            , verify=False
                            )
        print (resp.status_code)
        # print(json.dumps(resp.json(), indent=2))
        #
        respJson = resp.json()

        candidates = []
        for c in respJson["results"]:
            candidate = CandidateInfo(
                c["ID"],
                c["NAME"],
                c["DESIGNATION"],
                c["EXPERIENCE_SUMMARY"],
                c["INDUSTRY"],
                c["COUNTRY"],
                c["result_metadata"]["score"]
            )
            candidates.append(candidate)

        findCandResp = FindCandidatesResponse(respJson["matching_results"],candidates)
        return findCandResp

    def matchCandidates(self, queryString):
        discovery_api_query_url = 'https://gateway-wdc.watsonplatform.net/discovery/api/v1/environments/'\
                                  + app.config['DISCOVERY_ENVIRONMENT_ID']\
                                  + '/collections/'\
                                  + app.config['DISCOVERY_CONNECTIONS_COLLECTION_ID']\
                                  + '/query'

        reqParams = {"version" : app.config['DISCOVERY_API_VERSION'],
            'deduplicate' : 'false',
            'highlight' : 'false',
            # 'passages' : 'true',
            # 'passages.count' : '5',
            'natural_language_query' : queryString}
        print (reqParams)
        resp = requests.get( discovery_api_query_url
                            , params=reqParams
                            , auth=('apikey', app.config['DISCOVERY_API_KEY'])
                            , verify=False
                            )
        print (resp.status_code)
        # print(json.dumps(resp.json(), indent=2))
        #
        respJson = resp.json()

        candidates = []
        for c in respJson["results"]:
            candidate = CandidateInfo(
                c["ID"],
                c["NAME"],
                c["DESIGNATION"],
                c["EXPERIENCE_SUMMARY"],
                c["INDUSTRY"],
                c["COUNTRY"],
                c["result_metadata"]["score"]
            )
            candidates.append(candidate)

        findCandResp = FindCandidatesResponse(respJson["matching_results"],candidates)
        return findCandResp

    def matchJobs(self, queryString):
        discovery_api_query_url = 'https://gateway-wdc.watsonplatform.net/discovery/api/v1/environments/'\
                                  + app.config['DISCOVERY_ENVIRONMENT_ID']\
                                  + '/collections/'\
                                  + app.config['DISCOVERY_JOBS_COLLECTION_ID']\
                                  + '/query'

        reqParams = {"version" : app.config['DISCOVERY_API_VERSION'],
            'deduplicate' : 'false',
            'highlight' : 'false',
            # 'passages' : 'true',
            # 'passages.count' : '5',
            'count' : '26',
            'natural_language_query' : queryString}
        print (reqParams)
        resp = requests.get( discovery_api_query_url
                            , params=reqParams
                            , auth=('apikey', app.config['DISCOVERY_API_KEY'])
                            , verify=False
                            )
        print (resp.status_code)
        # print(json.dumps(resp.json(), indent=2))
        respJson = resp.json()
        jobs = []
        for c in respJson["results"]:
            str_title_category = ""
            for title_category in c["enriched_Title"]["categories"]:
                if(title_category["score"]>0.50):
                    str_title_category = str_title_category + title_category["label"]
            str_desc_category = ""
            for desc_category in c["enriched_Description"]["categories"]:
                if(desc_category["score"]>0.60):
                    str_desc_category = str_desc_category + desc_category["label"]
            job = JobInfo(
                c["JobId"],
                c["Title"],
                c["Description"],
                c["URL"],
                c["result_metadata"]["score"],
                str_title_category,
                str_desc_category
            )
            jobs.append(job)

        findJobResp = FindJobsResponse(respJson["matching_results"],jobs)
        return findJobResp

################################################################################
        # self.discovery = DiscoveryV1(
        #     version=app.config['DISCOVERY_API_VERSION'],
        #     username='apikey',
        #     password=app.config['DISCOVERY_API_KEY'],
        #     # iam_apikey=app.config['DISCOVERY_API_KEY'],
        #     url=app.config['DISCOVERY_API_URL']
        # )

    # def matchCandidates(self, queryString):
    #     self.discovery.set_detailed_response(True)
    #     print("{0}, {1}, {2}".format(app.config['DISCOVERY_ENVIRONMENT_ID'],
    #                                     app.config['DISCOVERY_COLLECTION_ID'],queryString))
    #     try:
    #         # Invoke a Discovery method
    #         response = self.discovery.query(app.config['DISCOVERY_ENVIRONMENT_ID'],
    #                                         app.config['DISCOVERY_COLLECTION_ID'], query=queryString)
    #
    #         # response = self.discovery.query(self, app.config['DISCOVERY_ENVIRONMENT_ID'], app.config['DISCOVERY_COLLECTION_ID'], filter=None, query=queryString, natural_language_query=None, passages=None,
    #         #       aggregation=None, count=None, return_fields=None, offset=None, sort=None, highlight=None,
    #         #       passages_fields=None, passages_count=None, passages_characters=None, deduplicate=None,
    #         #       deduplicate_field=None, collection_ids=None, similar=None, similar_document_ids=None, similar_fields=None,
    #         #       bias=None, logging_opt_out=None)
    #     except WatsonApiException as ex:
    #         print("Method failed with status code " + str(ex.code) + ": " + ex.message)
    #     else:
    #         print(json.dumps(response.get_result(), indent=2))
    #         print(response.get_headers())
    #         print(response.get_status_code())
    #     return None
