
from search_functions.functions import pathit
from search_functions.functions import getconf

# Assigns path to search. relative path is dominant
abs_path = getconf('location','search_abs')
rel_path = getconf('location','search_rel')
relpath = pathit(rel_path, ROOT=True)
my_path  = abs_path if not rel_path else relpath

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
