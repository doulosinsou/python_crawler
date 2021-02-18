import os
import json
from search_functions.functions import pathit
from configparser import ConfigParser
import mysql.connector

configur = ConfigParser()
file = pathit('../.config')
configur.read(file)

def scantree(path:str) -> dict:
    """Recursively yield DirEntry objects for given directory.
    :param path: str local directory to search
    :return: obj with data about the files, namely: file path

    """
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry


def droptables(*tables:list) -> None:
    """
    Removes tables from database speficied in config.
    :param tables: an array of table names to drop. If no array provided, then drop all lettered tables.
    """
    cred = configur._sections['mysql_credentials']
    cnx = mysql.connector.connect(**cred)
    cursor = cnx.cursor()

    if not tables:
        tables = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z"
    tables = "".join(map(str, tables))
    wipe = "DROP TABLE IF EXISTS {}".format(tables)
    cursor.execute(wipe)
    print("dropped the following tables: {}".format(tables))


want_clear_local = input("Do you want the clear local storage? type 'yes' or 'no'  ")
want_clear_local.lower()
if want_clear_local == 'yes':
    dir = os.getcwd()+"/index"
    for f in scantree(dir):
        if 'crawled.json' in f.path:
            # path = dir+"/"+f
            # with open(f.path,'r') as crawled:
            #     old = json.load(crawled)
            with open(f.path,'w') as crawled:
                blank = []
                json.dump(blank, crawled)
            continue
        print("Removing {}".format(f))
        os.remove(os.path.join(dir, f))
        if not os.path.isfile(os.path.join(dir, f)):
            print("successful")

    log = open('logfile.log', 'w').close()
else:
    print('keeping local data')
    print()

want_clear_sql = input("Do you want the clear SQL data? type 'yes' or 'no'  ")
want_clear_sql.lower()
if want_clear_sql == 'yes':
    droptables()
else:
    print('keeping sql data')
