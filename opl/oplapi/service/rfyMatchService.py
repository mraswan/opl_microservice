import logging
import requests
import urllib
import json


from ... import rfyAPIApp as app
from ..service.filterUtlityService import FilterUtilityService
from ..model.matchedjobs import MatchedJobs
from ..model.matchedcandidate import MatchedCandidate

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RfyMatchService(object):
    def __init__(self):
        self.counter = 0


    #Get job match for candidate
    def getJobMatchesForCandidate(self, project, title, description, senioritylevel, coordinates, country):
        if (description == None or description ==""):
            qValue = ''
        else:
            qValue = 'OR description:(' + description + ')^' + app.config['DESCRIPTION_BOOSTING_VALUE']

        reqParams = {"wt": "json",
                     "q": '(exact_title:(' + title + ') OR {!edismax  qf="title" v="' + title + '"})'
                            + qValue,
                     "rows":app.config['JOB_NO_OF_ROWS_FETCH'],
                     "fl": ' *, score, distance:geodist(coordinates,' + coordinates
                            + '),senLevDif:sub(seniorityLevel,' + senioritylevel + ')',
                     "fq": 'entity:Jobs AND '
                            +'country:"' + country +'"'
                            +' AND {!geofilt sfield=coordinates pt=' + coordinates
                            + ' d=' + app.config['DISTANCE_FILTER'] + '}'
                     }
        print (reqParams)
        resp = requests.get(app.config['SOLR_BASE'] +
                             app.config['SOLR_COLLECTION_'+project] +
                             app.config['SOLR_SELECT'], params=reqParams)

        print (resp.status_code, resp.json())

        retObj = resp.json()
        filterUtlityService = FilterUtilityService()
        solrRes = min(retObj['response']['numFound'], int(app.config['JOB_NO_OF_ROWS_FETCH']))
        masterList = []
        if (retObj['response']['numFound'] > 0):
            for response in range(0, solrRes):
                # print response
                score = filterUtlityService.normaliseSeniorityLevel(
                    float(retObj['response']['docs'][response]['senLevDif']),
                    float(retObj['response']['docs'][response]['score']))
                score = filterUtlityService.normaliseDistance(float(retObj['response']['docs'][response]['distance']),
                                                              score)
                retVal = MatchedCandidate(

                    retObj['response']['docs'][response]['id']
                    , (retObj['response']['docs'][response]['title']).encode('utf-8')
                    , '' #'(retObj['response']['docs'][response]['description']).encode('utf-8')
                    , retObj['response']['docs'][response]['distance']
                    , retObj['response']['docs'][response]['senLevDif']
                    , score
                    , resp.status_code
                )
                masterList.append(retVal)
        else:
            retVal = MatchedCandidate()
            masterList.append(retVal)
        return masterList


    # Get candidate match for job
    def getCandidateMatchesForJob(self, project, title, description1, senioritylevel, coordinates, country):
        description = description1
        if (description == None or description ==""):
            qValue = ''
        else:
            qValue = 'OR cand_description:(' + description + ')^' + app.config['DESCRIPTION_BOOSTING_VALUE']

        reqParams = {"wt": "json",
                     "q": '(cand_exact_title:(' + title + ') OR {!edismax  qf="cand_title" v="'
                            + title + '"})'
                            + qValue,
                     "rows":app.config['CANDIDATE_NO_OF_ROWS_FETCH'],
                     "fl": ' *, score, distance:geodist(coordinates,' + coordinates
                            + '),senLevDif:sub(seniorityLevel,' + senioritylevel + ')',
                     "fq": 'entity:Candidates AND '
                            +'cand_country:"' + country.encode('utf-8') +'" '
                            +' AND {!geofilt sfield=coordinates pt=' + coordinates
                            + ' d=' + app.config['DISTANCE_FILTER'] + '}'
                     }
        print (reqParams)
        resp = requests.get(app.config['SOLR_BASE'] +
                             app.config['SOLR_COLLECTION_'+project] +
                             app.config['SOLR_SELECT'], params=reqParams)

        print (resp.status_code, resp.json())

        retObj = resp.json()
        if not 'response' in retObj:
            return None

        solrRes = min(retObj['response']['numFound'], int(app.config['CANDIDATE_NO_OF_ROWS_FETCH']))
        masterList = []
        filterUtlityService = FilterUtilityService()
        if (retObj['response']['numFound'] > 0):
            for response in range(0, solrRes):
                score = filterUtlityService.normaliseSeniorityLevel(
                    float(retObj['response']['docs'][response]['senLevDif']),
                        float(retObj['response']['docs'][response]['score']))

                score = filterUtlityService.normaliseDistance(float(retObj['response']['docs'][response]['distance']),
                                                              score)
                try:
                    cand_description = (retObj['response']['docs'][response]['cand_description'])# .encode('utf8')
                except:
                    cand_description = None

                retVal = MatchedJobs(
                    retObj['response']['docs'][response]['id']
                    , (retObj['response']['docs'][response]['cand_title']).encode('utf-8')
                    , cand_description
                    , retObj['response']['docs'][response]['distance']
                    , retObj['response']['docs'][response]['senLevDif']
                    , score
                    , resp.status_code
                )
                masterList.append(retVal)
        else:
            retVal = MatchedJobs()
            masterList.append(retVal)
        return masterList


    # Data import to Solr
    def importDataToSolr(self, argsJson):

        if (argsJson.get("entity") == None):
            entityValue = ''
        else:
            entityValue = app.config['SOLR_DATA_IMPORT_ENTITY'] + argsJson.get("entity")

        if(argsJson.get("entity") == 'Jobs' and argsJson.get("clean") == 'false'):
            respdelete = urllib.urlopen(app.config['SOLR_BASE'] +
                                  app.config['SOLR_COLLECTION_' + argsJson.get("project")] +
                                  '/update?stream.body=<delete><query>entity:Jobs</query></delete>&commit=true'
                                 )
        print (respdelete.geturl())
        resp = urllib.urlopen(app.config['SOLR_BASE'] +
                            app.config['SOLR_COLLECTION_'+argsJson.get("project")] +
                            app.config['SOLR_DATA_IMPORT'] +
                            app.config['SOLR_DATA_IMPORT_COMMAND'] + argsJson.get("command") +
                            entityValue +
                            app.config['SOLR_DATA_IMPORT_CLEAN'] + argsJson.get("clean")
                            )
        print (resp.url)

        Rfy=RfyMatchService()
        data=Rfy.checkDataImportStatus(argsJson)
        print ("Started Data Import")
        print ("Solr is "+ data['status']+ ". Data Import "+ data['importResponse']+" Please wait till indexing is done in solr")

        while (data['status']=='busy' and data['importResponse']=='A command is still running...'):
            data = Rfy.checkDataImportStatus(argsJson)
            #time pass

        print (data)
        return data


    #Check the status of data import
    def checkDataImportStatus(self, argsJson):
        importstatus = urllib.urlopen(app.config['SOLR_BASE'] +
                                      app.config['SOLR_COLLECTION_' + argsJson.get("project")] +
                                      app.config['SOLR_DATA_IMPORT'] +
                                      app.config['SOLR_DATA_IMPORT_COMMAND'] + 'status&wt=json')
        #print importstatus.geturl()
        data = json.loads(importstatus.read())
        return data