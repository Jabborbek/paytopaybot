
import sqlite3


class SQLither:

    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.c = self.conn.cursor()





