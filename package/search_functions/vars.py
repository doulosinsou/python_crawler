# import search_functions.functions as functions
from search_functions.functions import pathit
from search_functions.functions import getconf
# from configparser import ConfigParser
#
# configur = ConfigParser()
# file = pathit('../.config')
# configur.read(file)

my_path = pathit(getconf('location','search_path'), ROOT=True)

index_path = pathit(getconf('location','index_path'), ROOT=True)

exclude_all = getconf('exclude','paths', line=True)+getconf('exclude','files', line=True)
include_text = getconf('include','text',line=True)

include_all = getconf('include', 'non-text',line=True)+include_text

exclude_words = open(pathit('exclude_words.txt')).read().splitlines()

crawled = pathit('index/crawled.json', ROOT=True)

num_files = 0
num_dir = 0
num_words = 0
num_purge = 0
