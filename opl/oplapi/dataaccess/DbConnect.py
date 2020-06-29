import sqlite3
from sqlite3 import Error

class DbConnect:
    def __init__(self, dbFile):
        print("Initialize DbConnect")
        self.dbFile = dbFile

    def _createConnection(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.dbFile)
            # print("sqlite3.version = {}, from class: {}".format(sqlite3.version, self.__class__.__name__))
        except Error as e:
            print(e)
        return conn

