import os
import json
import search_functions.vars as vars


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


# dir = os.getcwd()+"/index"
dir = vars.index_path
for f in scantree(dir):
    print("Removing {}".format(f))
    os.remove(os.path.join(dir, f))
    if not os.path.isfile(os.path.join(dir, f)):
        print("successful")

log = open('logfile.log', 'w').close()
