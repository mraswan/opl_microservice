# import sqlite3
from sqlite3 import Error
# from conf import config
from ..dataaccess.DbConnect import DbConnect
# from model import App
from opl import oplAPIApp as app
from opl.oplapi.model.category import Category


class CategoryDataAccess(DbConnect):

    def __init__(self, dbFile):
        super().__init__(dbFile)
        print("Initialize CategoryDataAccess")

    # def create(self):
    #     """ create a table from the create_table_sql statement
    #     :param conn: Connection object
    #     :param create_table_sql: a CREATE TABLE statement
    #     :return:
    #     """
    #     retVal = False
    #     try:
    #         conn = self._createConnection()
    #         with conn:
    #             c = conn.cursor()
    #             print("Executing SQL(s) {} ...".format(config.SQL_CREATE_TABLE_APP))
    #             c.execute(config.SQL_CREATE_TABLE_APP)
    #             print("Executing SQL(s) {} ...".format(config.SQL_CREATE_INDEX_APP_ID))
    #             c.execute(config.SQL_CREATE_INDEX_APP_ID)
    #             print("Executing SQL(s) {} ...".format(config.SQL_CREATE_INDEX_APP_NAME))
    #             c.execute(config.SQL_CREATE_INDEX_APP_NAME)
    #             print("Executing SQL(s) {} ...".format(config.SQL_CREATE_INDEX_APP_QUEUE))
    #             c.execute(config.SQL_CREATE_INDEX_APP_QUEUE)
    #             print("Executing SQL(s) {} ...".format(config.SQL_CREATE_INDEX_APP_USER))
    #             c.execute(config.SQL_CREATE_INDEX_APP_USER)
    #             print("Executing SQL(s) {} ...".format(config.SQL_CREATE_INDEX_APP_START_TIME))
    #             c.execute(config.SQL_CREATE_INDEX_APP_START_TIME)
    #             print("Executing SQL(s) {} ...".format(config.SQL_CREATE_INDEX_APP_END_TIME))
    #             c.execute(config.SQL_CREATE_INDEX_APP_END_TIME)
    #             retVal = True
    #             print("Table and Index creation successful!!!");
    #     except Error as e:
    #         print(e)
    #     return retVal

    # app ( id,
    #         app_id,
    #         user,
    #         name,
    #         app_type,
    #         queue,
    #         start_time,
    #         end_time,
    #         state,
    #         final_state,
    #         tracking_url )
    # def insert(self, app):
    #     """
    #     Insert a new app
    #     :param conn:
    #     :param app:
    #     :return: id
    #     """
    #     retVal = -1
    #     try:
    #         conn = self._createConnection()
    #         with conn:
    #             sql = config.SQL_INSERT_APP
    #             # print("Executing SQL(s): {}\n\t{}...".format(sql, app))
    #             cur = conn.cursor()
    #             cur.execute(sql, (app.app_id,
    #                                 app.user,
    #                                 app.name,
    #                                 app.app_type,
    #                                 app.queue,
    #                                 app.start_time,
    #                                 app.end_time,
    #                                 app.state,
    #                                 app.final_state,
    #                                 app.tracking_url,
    #                                 app.memory_seconds,
    #                                 app.vcore_seconds,
    #                                 app.preempted_mem_gb,
    #                                 app.preempted_vcores
    #                               ))
    #             app.id = cur.lastrowid
    #             retVal = cur.lastrowid
    #     except Error as e:
    #         print(e)
    #     return retVal

    def selectAllCategories(self):
        """
        Query tasks by priority
        :param conn: the Connection object
        :return:Category
        """
        categories = []
        conn = self._createConnection()
        with conn:
            sql = app.config['SQL_SELECT_CATEGORY_SUB_CATEGORY']
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            category = None
            prev_id = 0
            for row in rows:
                if (row[0] != prev_id):
                    category = Category(row[0], row[1])
                    categories.append(category)
                    prev_id = row[0]
                category.addSubCategory(row[2], row[3])
        return categories

    # def selectByName(self, name):
    #     """
    #     Query tasks by priority
    #     :param conn: the Connection object
    #     :return:App[]
    #     """
    #     app = None
    #     conn = self._createConnection()
    #     with conn:
    #         sql = config.SQL_SELECT_APPS_BY_NAME
    #         cur = conn.cursor()
    #         cur.execute(sql, (name,))
    #         apps = [App.App(*row) for row in cur.fetchall()]
    #     return apps
    #
    # def selectByAppID(self, appId):
    #     """
    #     Query tasks by priority
    #     :param conn: the Connection object
    #     :return:App
    #     """
    #     app = None
    #     conn = self._createConnection()
    #     with conn:
    #         sql = config.SQL_SELECT_APP_BY_APP_ID
    #         cur = conn.cursor()
    #         cur.execute(sql, (appId,))
    #         rows = cur.fetchall()
    #         for row in rows:
    #             # pprint(row)
    #             app = App.App(*row)
    #             break
    #     return app
    #
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
