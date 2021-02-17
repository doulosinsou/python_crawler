import os
import json
from search_functions.functions import droptables
import mysql.connector

def scantree(path:str) -> dict:
    """Recursively yield DirEntry objects for given directory.
    Dependencies: [
    os,
    exclude_path(local),
    ]
    :param path: str local directory to search
    :return: obj with data about the files, namely: file path

    """
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry



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

# droptables()
