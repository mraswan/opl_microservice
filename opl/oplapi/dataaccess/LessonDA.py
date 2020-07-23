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

    def selectAllLessons(self):
        """

        :param
        :return:Lesson
        """
        lessons = []
        conn = self._createConnection()
        with conn:
            sql = app.config['SQL_SELECT_LESSON']
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
