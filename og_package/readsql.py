from search_functions.sql_ite3 import *

sl = sql_ite('index/crawled.db')



inp = str(input("Find a word in the database: "))
fl = inp[0]

join = """
SELECT word, title, count, in_title
FROM {0}
INNER JOIN crawled on crawled.rowid = {0}.id
WHERE word='{1}'
""".format(fl,inp)
sel = "SELECT * FROM {} WHERE word='{}'".format(fl, inp)
a = sl.select(join)

for w in a:
    print(w)
    # newset = {w['id'] for w in a}
    # for ids in newset:
    #

sl.close()
