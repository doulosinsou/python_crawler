
import mysql.connector
import os
import json
import time
from colors import *
from configparser import ConfigParser
from functions import pathit

configur = ConfigParser()
file = pathit('../.config')
configur.read(file)


def create(db:str) -> None:
    """Creates a mysql table [if exists] withtin the database specified in the config file"""
    cred = configur._sections['mysql_credentials']
    cnx = mysql.connector.connect(**cred)
    cursor = cnx.cursor()
    baseline = (
    "CREATE TABLE IF NOT EXISTS `{}` ("
    "  `id` int(6) NOT NULL AUTO_INCREMENT,"
    "  `word` varchar(25) NOT NULL,"
    "  `title` varchar(75) NOT NULL,"
    "  `file_path` varchar(400) NOT NULL,"
    "  `score` int(4) NOT NULL,"
    "  `in_title` int(4) NOT NULL,"
    "  `modified` date NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB".format(db))
    try:
        cursor.execute(baseline)
        # print_green("created table: "+db)
    except mysql.connector.Error as err:
        print(err.msg)
    cursor.close()
    cnx.close()


def postit(db:str, post:str) -> None:
    """
    Post a block of entries into appropriate table.
    :param db: a string of the table name
    :param post: a stringed series of tuples. Each tuple is a new row to post.
    """
    cred = configur._sections['mysql_credentials']
    cnx = mysql.connector.connect(**cred)
    cursor = cnx.cursor()


    def exists(table, full):
        query = ("SELECT score FROM {} "
        "WHERE word='{}' "
        "AND file_path='{}'"
        .format(table, full[0], full[2]))
        cursor.execute(query)
        answer = cursor.fetchall()
        if answer:
            return answer[0][0]
        else:
            return 0


    def insert(table, full):

        add_entry = ("INSERT INTO {} "
               "(word, title, file_path, score, in_title, modified) "
               "VALUES{}"
               .format(table,full))
        # print_yellow(add_entry)
        cursor.execute(add_entry)
        cnx.commit()
        print('inserted {}'.format(full[0]))


    def update(table, full):
        add_entry = ("UPDATE {} "
               "SET score={} "
               "WHERE word='{}' "
               "AND file_path='{}'"
               .format(table,full[3],full[0],full[2]))
        # print_yellow(add_entry)
        cursor.execute(add_entry)
        cnx.commit()
        # print('updated {}'.format(full[0]))


    for full in post:
        score = exists(db, full)
        if score == 0:
            insert(db, full)
        elif score != int(full[3]):
            update(db, full)

    cursor.close()
    cnx.close()


def removeit(db:str, post:dict) -> None:
    """Remove a set of words from a table.
    :param db: the name of the table
    :param post: a dictionary defining the key 'word' to remove and key 'file_path' to match the instance of the word to remove.
    """
    cred = configur._sections['mysql_credentials']
    cnx = mysql.connector.connect(**cred)
    cursor = cnx.cursor()
    delete_entry = ("DELETE FROM {} WHERE {}='{}' AND {}='{}'".format(db, 'word', post['word'], 'file_path', post['file_path']))
    cursor.execute(delete_entry)
    cnx.commit()
    cursor.close()
    cnx.close()


def droptables(tables:list) -> None:
    """
    Removes tables from database speficied in config.
    :param tables: an array of table names to drop. If no array provided, then drop all lettered tables.
    """
    cred = configur._sections['mysql_credentials']
    cnx = mysql.connector.connect(**cred)
    cursor = cnx.cursor()

    if not tables:
        tables = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]
    tables = "".join(map(str, tables))
    wipe = "DROP TABLE IF EXISTS {}".format(tables)
    cursor.execute(wipe)


def grabdata():
    for file in os.scandir(pathit('../index')):
        if 'store.json' not in file.name:
            continue
        path = str(file.path)
        with open(path, 'r') as wordlist:
            words = json.load(wordlist)
        data = (file.name[0], words)
        yield data


start_timer = time.perf_counter()
for dataset in grabdata():
    mini_timer = time.perf_counter()
    fletter = dataset[0]
    words = dataset[1]
    # print_yellow("now filing: "+fletter)

    words_list = []
    for word in words:

        for i in words[word]:
            newtup = (word, i['title'], i['file_path'], str(i['score']), str(i['in_title']), i['modified'])
            words_list.append(newtup)

    create(fletter)
    postit(fletter,words_list)

    end_mini_timer = time.perf_counter()
    total_mini = end_mini_timer - mini_timer
    print_green("successfully updated letter {} in {:0.4}s".format(fletter, total_mini))

end_timer = time.perf_counter()
total_timer = end_timer - start_timer
print_yellow("successfully updated all letters in {:0.4}s".format(total_timer))
