import sqlite3
import json

class sql_ite:
    """Establishes connection and executes calls to local database"""
    def __init__(self):
        self.connection = sqlite3.connect('index/crawled.db')
        self.c = self.connection.cursor()
        name = "crawled"
        cols = "path text, title text, mod integer, list blob"
        self.makeTable(name, cols)

    def doit(self, thing):
        try:
            self.c.execute(thing)
        except sqlite3.OperationalError as err:
            print(err)

    def makeTable(self, name, cols):
        createT = "CREATE TABLE {0}({1})".format(name, cols)
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

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()



slite = sql_ite()

fletter = "a"
blob = json.dumps(['this','is','a','list'])
newcrawled = ('path/goes/here','my path',20210301,blob)

slite.makeFletter(fletter)
slite.addRow('crawled', newcrawled)

id = slite.id()[0]
newRowData = (id, 'aakbar', 5, 0)
slite.addRow(fletter, newRowData)

slite.commit()
slite.c.execute("SELECT * FROM a WHERE word=?",('aakbar',))
stuff = slite.c.fetchall()
for s in stuff:
    print(s)


slite.close()
