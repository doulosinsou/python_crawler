import sqlite3
import search_functions.vars as vars
# import json

class sql_ite:
    """Establishes connection and executes calls to local database"""
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.c = self.connection.cursor()
        name = "crawled"
        cols = "id INTEGER PRIMARY KEY, path TEXT, title TEXT, mod INTEGER, list BLOB, active INTEGER DEFAULT 1"
        self.makeTable(name, cols)

    def doit(self, thing):
        try:
            self.c.execute(thing)
        except sqlite3.OperationalError as err:
            print(err)

    def makeTable(self, name, cols):
        createT = "CREATE TABLE IF NOT EXISTS {0}({1})".format(name, cols)
        self.doit(createT)

    def addRow(self, table, content):
        createR = "INSERT INTO {0} VALUES{1}".format(table, content)
        self.doit(createR)

    def makeFletter(self, fletter):
        cols = "id integer, word text, count integer, in_title integer"
        self.makeTable(fletter, cols)

    def id(self):
        find = "SELECT last_insert_rowid() from crawled"
        self.doit(find)
        return self.c.fetchone()

    def select(self, terms, fetchall=True):
        self.c.execute(terms)
        if fetchall:
            return self.c.fetchall()
        else:
            return self.c.fetchone()


    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()



sl = sql_ite(vars.crawled)
