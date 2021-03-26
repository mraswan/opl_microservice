from sqlite3 import Error
from ..dataaccess.DbConnect import DbConnect
from opl import oplAPIApp as app
from opl.oplapi.model.user import User, Contributor

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

    def selectContributorByUserhandle(self, user_handle):
        contributor = None
        conn = self._createConnection()
        try:
            with conn:
                sql = app.config['SQL_SELECT_CONTRIBUTOR_BY_USER_HANDLE']
                cur = conn.cursor()
                cur.execute(sql, (user_handle,))
                row = cur.fetchone()
                if row is not None:
                    contributor = Contributor(*row)
        except Error as e:
            print(e)
        return contributor

    def selectContributorByUserId(self, user_id):
        contributor = None
        conn = self._createConnection()
        try:
            with conn:
                sql = app.config['SQL_SELECT_CONTRIBUTOR_BY_ID']
                cur = conn.cursor()
                cur.execute(sql, (user_id,))
                row = cur.fetchone()
                if row is not None:
                    contributor = Contributor(*row)
        except Error as e:
            print(e)
        return contributor


    def selectContributors(self):
        contributors = None
        conn = self._createConnection()
        try:
            with conn:
                sql = app.config['SQL_SELECT_CONTRIBUTORS']
                cur = conn.cursor()
                cur.execute(sql,)
                contributors = [Contributor(*row) for row in cur.fetchall()]
        except Error as e:
            print(e)
        return contributors

    def selectContributorsAndSkills(self):
        contributors_sills = {}
        conn = self._createConnection()
        try:
            with conn:
                sql = app.config['SQL_SELECT_CONTRIBUTORS_N_SKILLS']
                cur = conn.cursor()
                cur.execute(sql,)
                # contributors = [Contributor(*row) for row in cur.fetchall()]
                rows = cur.fetchall();
                for row in rows:
                    if row[0] not in contributors_sills:
                        skill_n_counts = {row[1]: 1}
                        contributors_sills[row[0]] = skill_n_counts
                    else:
                        skill_n_counts = contributors_sills[row[0]]
                        if row[1] not in skill_n_counts:
                            skill_n_counts[row[1]] = 1
                        else:
                            skill_n_counts[row[1]] = skill_n_counts[row[1]] + 1
        except Error as e:
            print(e)
        return contributors_sills

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
