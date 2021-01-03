import sqlite3

 
class SQLighter():
    def __init__(self, database):
        self.database = database

    def execute(self, sql, values=[]):
        with sqlite3.connect(self.database, check_same_thread=False) as conn:
            conn.execute(sql, values)
 
    def select(self, sql, values=[]):
        with sqlite3.connect(self.database, check_same_thread=False) as conn:
            return list(conn.execute(sql, values))