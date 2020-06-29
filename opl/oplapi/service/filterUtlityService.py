import pymysql

from ... import rfyAPIApp as app



class FilterUtilityService:

    def __init__(self):
        print ("Post solr response normalization methods")


    def normaliseSeniorityLevel(self, senlevdif, solrscore):
        if (senlevdif == 0):
            score = solrscore
        elif (senlevdif == 1):
            score = solrscore * 0.9
        else:
            score = solrscore * 0.6

        return score


    def normaliseDistance(self, distance, after_sl_score):
        if (distance <= 250):
            score = after_sl_score
        elif (distance > 250 and distance <= 500):
            score = after_sl_score * 0.95
        elif (distance > 500 and distance <= 1000):
            score = after_sl_score * 0.9
        elif (distance > 1000 and distance <= 2000):
            score = after_sl_score * 0.85
        elif (distance > 2000 and distance <= 3000):
            score = after_sl_score * 0.8

        return score


    def getMysqlDbConnection(self, project_name):
        myConnection = pymysql.connect(host=app.config['DATABASE_HOSTNAME'], user=app.config['DATABASE_USERNAME'],
                        passwd=app.config['DATABASE_PASSWORD'], db=app.config['DATABASE_NAME_' + project_name])
        return myConnection
