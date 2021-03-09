import sqlite3
import os
import sys


def droptables(path):
    c = sqlite3.connect(path)
    cur = c.cursor()

    tables = """
    SELECT name
    FROM sqlite_master
    WHERE
    type ='table'
    AND name NOT LIKE 'sqlite_%'
    """


    def tabs():
        cur.execute(tables)
        tabs = cur.fetchall()
        for t in tabs:
            yield t[0]


    for n in tabs():
        print('dropping {}'.format(n))
        drop = "drop table if exists {}".format(n)
        cur.execute(drop)

    # cur.executemany("DROP TABLE IF EXISTS ? ", tabs())
    # cur.execute("drop table if exists scrape")

    c.commit()


def destroytable(path):
    os.remove(path)


dir = "index/"
while True:
    tab = str(input("enter database: "))
    db = dir+tab+".db"
    if tab.lower() == "exit":
        sys.exit()
    if not os.path.exists(db):
        print("invalid database")
    else:
        break

print("""
0:cancel
1:drop all tables in {}
2:delete database
""".format(db))

while True:
    choose = int(input())
    if choose == 0:
        print("Exiting")
        break
    elif choose == 1:
        droptables(db)
        print("Dropped tables from {}".format(db))
        break
    elif choose == 2:
        destroytable(db)
        print("Deleted {}".format(db))
        break
