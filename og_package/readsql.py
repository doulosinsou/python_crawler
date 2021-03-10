from search_functions.sql_ite3 import *

sl = sql_ite('index/crawled.db')


while True:
    inp = str(input("Find a word in the database: ").lower())
    fl = inp[0]
    if inp == "quit" or inp == "exit":
        break

    join = """
    SELECT word, title, count, in_title
    FROM {0}
    INNER JOIN crawled on crawled.rowid = {0}.id
    WHERE word=?
    """.format(fl)

    a = sl.select(join, (inp,))

    for w in a:
        print(w['word'], w['title'])
        # newset = {w['id'] for w in a}
        # for ids in newset:
        #

sl.close()
