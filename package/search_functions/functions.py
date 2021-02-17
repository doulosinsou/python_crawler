from configparser import ConfigParser

def pathit(path:str, ROOT=False):
    import os
    if ROOT:
        file = os.path.join(os.getcwd(), path)
        return file
    else:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, path)
        return my_file


def getconf(section:str, key:str, line=False, bool=False):
    if bool:
        return configur.getboolean(section,key)
    if line:
        return configur.get(section,key).strip().splitlines()
    else:
        return configur.get(section,key)




configur = ConfigParser()
file = pathit('../.config')
configur.read(file)


import mysql.connector


def create(db):
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
    except mysql.connector.Error as err:
        print(err.msg)
    cursor.close()
    cnx.close()

def postit(db, post):
    cred = configur._sections['mysql_credentials']
    cnx = mysql.connector.connect(**cred)
    cursor = cnx.cursor()
    add_entry = ("INSERT INTO {} "
           "(word, title, file_path, score, in_title, modified) "
           "VALUES{}".format(db, post))
    cursor.execute(add_entry)
    cnx.commit()
    cursor.close()
    cnx.close()


def removeit(db, post):
    cred = configur._sections['mysql_credentials']
    cnx = mysql.connector.connect(**cred)
    cursor = cnx.cursor()
    delete_entry = ("DELETE FROM {} WHERE {}='{}' AND {}='{}'".format(db, 'word', post['word'], 'file_path', post['file_path']))
    cursor.execute(delete_entry)
    cnx.commit()
    cursor.close()
    cnx.close()


def droptables():
    cred = configur._sections['mysql_credentials']
    cnx = mysql.connector.connect(**cred)
    cursor = cnx.cursor()

    wipe = "DROP TABLE IF EXISTS F,p,t "
    cursor.execute(wipe)
