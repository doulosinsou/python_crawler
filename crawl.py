import os
import re
import string
import json
import time

from bs4 import BeautifulSoup
from colors import *
from log import *

num_files = 0
num_dir = 0
num_words = 0

def call_files(dir="./test_files") -> None:
    """
    Compiles each file in directory. Sends to `crawl()` for parsing.
    Dependencies [
    os,
    scantree (local),
    crawl (local)
    ]

    :param dir: str of relative directory to search
    """
    for files in scantree(dir):
        rel_file = os.path.relpath(files.path, dir)
        local_path = "{}/{}".format(dir,rel_file)
        if already_crawled(local_path):
            print(local_path+" already crawled")
            continue
        crawl(local_path)


def scantree(path:str) -> dict:
    """Recursively yield DirEntry objects for given directory.
    Dependencies: [
    os,
    exclude_path(local),
    ]
    :param path: str local directory to search
    :return: obj with data about the files, namely: file path

    """
    global num_dir
    global num_files
    for entry in os.scandir(path):
        if exclude_path(entry.path) == False:
            continue
        if entry.is_dir(follow_symlinks=False):
            num_dir += 1
            yield from scantree(entry.path)
        else:
            if include_file_type(entry.path):
                continue
            num_files += 1
            yield entry


def already_crawled(file:str) -> True:
    modified = str(os.path.getmtime(file))
    crawled = './index/crawled.json'
    with open(crawled) as cfiles:
        flist = json.load(cfiles)
        for f in flist:
            fsplit = f.split('_MOD_')
            path = fsplit[0]
            mod = fsplit[1]
            if (path == file) and (mod == modified):
                return True
        flist.append(file+"_MOD_"+modified)
    with open(crawled, 'w') as cfiles:
        json.dump(flist, cfiles, indent=4, sort_keys=True)
    return False


def crawl(haystack:str) -> None:
    """Creates an index for every significant word used in supplied file. Scores the word by how many times it is used plus if it occurs in title of html.
    Dependencies{
    string,
    json,
    BeautifulSoup,
    os,
    exclude_word (local),
    }
    :param haystack: str path to file
    """
    global num_words
    # print_yellow("about to crawl: "+haystack)
    tic = time.perf_counter()
    modified = time.ctime(os.path.getmtime(haystack))

    with open('include.txt', 'r') as includes:
        text_files = includes.read().lower().splitlines()

    inc_list = []
    for lin in text_files:
        if "non-text:" in lin:
            break
        if "text:" in lin:
            continue
        if lin:
            inc_list.append(lin)

    if any(x in haystack for x in inc_list):
        with open(haystack, 'rb') as file:
            soup = BeautifulSoup(file, 'html.parser')

            content = str(soup.get_text()).lower()
            content = re.sub(r'[^a-zA-Z\s]+','',content)
            try:
                title = soup.find('title').string.lower()
            except:
                title = os.path.splitext(os.path.basename(haystack))[0]
    else:
        content = os.path.splitext(os.path.basename(haystack))[0]
        content = re.sub(r'[^a-zA-Z\s]+','',content).lower()
        title = content

    for word in content.split():
        if exclude_word(word) == False:
            continue

        word_score = count_words(word, content.split())
        in_title = count_words(word, title.split())

        first_letter = str(word[0])

        dump_file = "index/{}_dump.json".format(first_letter)
        if os.path.exists(dump_file) == False:
            f = open(dump_file, 'w')
            baseline = {}
            f.write(json.dumps(baseline))
            f.close()

        with open(dump_file) as dump_data:
            words_list = json.load(dump_data)

            if word not in words_list:
                words_list[word] =[]

            exists = 0
            for item in words_list[word]:
                if (item['title'] == title) and (item['score'] == word_score):
                    exists += 1

            if exists:
                continue

            new_data = {
                "title":str(title),
                "file_path":haystack,
                "score":word_score,
                "in_title":in_title,
                "modified":modified
            }

            words_list[word].append(new_data)

        if exists:
            continue
        with open(dump_file,'w') as stuff:
             json.dump(words_list, stuff, indent=4, sort_keys=True)

        num_words += 1
        # print("successfully scraped "+Color.B_White+Color.F_Black+word+Color.F_Default+Color.B_Default)
    toc = time.perf_counter()
    print_green("Crawled {} in {:0.4f} seconds".format(haystack, toc-tic) )


def exclude_path(file:str) -> False:
    type = "exclude_path.txt"

    """return False if supplied path matches any line in exclusion file"""
    exclude_path = list(open(type).read().splitlines())
    for ex in exclude_path:
        if ex in file: ## must be in to match part of path rather than all of it
            return False
    return True


def exclude_word(file:str) -> False:
    type = "exclude_words.txt"

    """return False if supplied word matches any word in exclusion file"""
    exclude_path = list(open(type).read().splitlines())
    for ex in exclude_path:
        if ex == file: ##must be == to match whole word rather than part of it
            return False
    return True


def count_words(needle:str, haystack:list) -> int:
    """Counts how many times str needle is exact match to haystack list items"""
    man_count = 0
    for n in haystack:
        man_count += 1 if n == needle else 0
    return man_count


def include_file_type(file:str) -> False:
    type = "include.txt"

    """return False if supplied file fails to match any file extention in inclusion file"""
    include_path = list(open(type).read().splitlines())
    for inc in include_path:
        if file.lower().endswith("."+inc.split('.')[-1]):
            return False
    return True


#**********************************************************
#begin calling code and time it
date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print(date)
search_dir = open('my_path.txt', 'r').read().strip()

start_timer = time.perf_counter()
call_files(search_dir) #this starts it all
end_timer = time.perf_counter()
total_time = end_timer-start_timer

print_yellow("Crawled {} files and {} directories.\nIndexed {} words.".format(num_files, num_dir, num_words))
print_green("Total time: {:0.4}s".format(total_time))

endfile = " end file ".center(80, "*")
print(endfile, "\n")
