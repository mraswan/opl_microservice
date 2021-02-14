from sqlite3 import Error
from ..dataaccess.DbConnect import DbConnect
from opl import oplAPIApp as app
from opl.oplapi.model.user import User

class UserDataAccess(DbConnect):

    def selectById(self, id):
        user = None
        conn = self._createConnection()
        try:
            with conn:
                sql = app.config['SQL_SELECT_USER_BY_ID']
                cur = conn.cursor()
                cur.execute(sql, (id,))
                row = cur.fetchone()
                if row is not None:
                    user = User(*row)
        except Error as e:
            print(e)
        return user

    def selectByGoogleId(self, google_id):
        user = None
        conn = self._createConnection()
        try:
            with conn:
                sql = app.config['SQL_SELECT_USER_BY_GOOGLE_ID']
                cur = conn.cursor()
                cur.execute(sql, (google_id,))
                row = cur.fetchone()
                if row is not None:
                    user = User(*row)
        except Error as e:
            print(e)
        return user

    def selectByEmail(self, email):
        user = None
        conn = self._createConnection()
        try:
            with conn:
                sql = app.config['SQL_SELECT_USER_BY_EMAIL']
                cur = conn.cursor()
                cur.execute(sql, (email,))
                row = cur.fetchone()
                if row is not None:
                    user = User(*row)
        except Error as e:
            print(e)
        return user

    def update_google_info(self, user):
        retVal = -1
        try:
            conn = self._createConnection()
            with conn:
                sql = app.config['SQL_UPDATE_GOOGLE_INFO']
                cur = conn.cursor()
                cur.execute(sql,
                            (user.name,
                             user.display_name,
                             user.google_id,
                             user.profile_pic,
                             user.email))
                retVal = 0
        except Error as e:
            print(e)
        return retVal

    def insert(self, user):
        retVal = -1
        try:
            conn = self._createConnection()
            with conn:
                sql = app.config['SQL_INSERT_USER']
                cur = conn.cursor()
                cur.execute(sql,
                            (user.email,
                             user.name,
                             user.display_name,
                             user.google_id,
                             user.profile_pic,
                             user.user_type_id))
                user.id = cur.lastrowid
                retVal = cur.lastrowid
        except Error as e:
            print(e)
        return retVal
