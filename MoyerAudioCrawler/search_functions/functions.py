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
