import sqlite3
import json

connection = sqlite3.connect('index/test.db')
cursor = connection.cursor()

createT = """
CREATE TABLE scrape
(word text, path text, title text, count integer, in_title integer, list blob)
"""
try:
    cursor.execute(createT)
except sqlite3.OperationalError as err:
    print(err)


addR = """
INSERT INTO scrape VALUES(?,?,?,?,?,?)
"""
blob = json.dumps(['this','is','a','list'])
addV = ('aakbar','this_path/index/','alderan',1,1,blob,)

cursor.execute(addR, addV)
connection.commit()


cursor.execute("SELECT * FROM scrape WHERE word=?",('aakbar',))
stuff = cursor.fetchall()
for s in stuff:
    print(s)

connection.close()
