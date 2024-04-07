import sqlite3

class DBconnector:
    def __init__(self,db_path):
        self.db_path = db_path

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        return conn