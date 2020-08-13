# import sqlite3
from sqlite3 import Error
# from conf import config
from ..dataaccess.DbConnect import DbConnect
# from model import App
from opl import oplAPIApp as app
from opl.oplapi.model.lesson import Lesson


class LessonDataAccess(DbConnect):

    def __init__(self, dbFile):
        super().__init__(dbFile)
        print("Initialize CategoryDataAccess")

    def selectAllLessons(self,offset, row_count):
        """

        :param
        :return:Lesson
        """
        lessons = []
        conn = self._createConnection()
        with conn:
            sql = app.config['SQL_SELECT_LESSON'].format(offset, row_count)
            cur = conn.cursor()
            cur.execute(sql)
            lessons = [Lesson(*row) for row in cur.fetchall()]
            # rows = cur.fetchall()
            # lesson = None
            # for row in rows:
            #     lesson = Lesson(*row)
            #     lessons.append(lesson)
        return lessons

    def selectLessonsCount(self):
        record_count = 0
        conn = self._createConnection()
        with conn:
            sql = app.config['SQL_SELECT_LESSON_COUNT'].format(offset, row_count)
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                record_count = row
                break
        return record_count

    def findLessons(self,query):
        """

        :param
        :return:Lesson
        """
        lessons = []
        conn = self._createConnection()
        with conn:
            sql = app.config['SQL_SELECT_FIND_LESSON'].format(query,query,query,query,0,app.config['SQL_ROW_COUNT'])
            cur = conn.cursor()
            cur.execute(sql)
            lessons = [Lesson(*row) for row in cur.fetchall()]
            # rows = cur.fetchall()
            # lesson = None
            # for row in rows:
            #     lesson = Lesson(*row)
            #     lessons.append(lesson)
        return lessons

    # def selectAppsNotProcessedForBinningApp(self):
    #     apps = []
    #     conn = self._createConnection()
    #     with conn:
    #         sql = config.SQL_SELECT_APPS_NOT_PROCESSED_FOR_BINNING_APP
    #         # print(sql)
    #         cur = conn.cursor()
    #         cur.execute(sql)
    #         apps = [App.App(*row) for row in cur.fetchall()]
    #     return apps
    #
    # def updateAppUrl(self, appId, urlValue):
    #     """
    #     Delete a task by task id
    #     :param conn:  Connection to the SQLite database
    #     :param id: id of the task
    #     :return:
    #     """
    #     conn = self._createConnection()
    #     with conn:
    #         sql = config.SQL_UPDATE_APP_URL
    #         cur = conn.cursor()
    #         cur.execute(sql, (urlValue, appId))
    #         conn.commit()
