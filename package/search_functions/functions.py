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


def getconf(section:str, key:str, line=False):
    get = configur.get(section,key)
    if line:
        return get.strip().splitlines()
    else:
        return get


configur = ConfigParser()
file = pathit('../.config')
configur.read(file)
