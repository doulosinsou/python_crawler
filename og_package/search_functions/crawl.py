import os
import re
import string
import json
import time

from bs4 import BeautifulSoup
from search_functions.colors import *
from search_functions.log import *


import search_functions.vars as vars
import search_functions.functions as functions
from search_functions.sql_ite3 import *
# from search_functions.vars import *

def call_files(dir="./test_files") -> None:
    """
    Compiles each file in directory. Sends to `crawl()` for parsing.
    :param dir: str of directory to search
    """
    #start by resetting the active status of pre-crawled pages.
    clear_active()
    for files in scantree(dir):
        #to ignore unnecessary repeats
        if already_crawled(files.path):
            print(files.path+" already crawled")
            continue
        vars.num_files += 1
        crawl(files.path)
    #remove words from paths that have been deleted
    del_inactive()
    sl.close()


def scantree(path:str) -> dict:
    """
    Recursively yield DirEntry objects for given directory.
    :param path: str local directory to search
    :return: obj with data about the files, namely: file path
    """

    for entry in os.scandir(path):
        #ignore paths/files on exclude list
        local = "/"+entry.path.split('/')[-1]+"/"
        if any(ex in local for ex in vars.exclude_all):
            # print_yellow(entry.path)
            continue
        #recurse through directories
        if entry.is_dir(follow_symlinks=False):
            vars.num_dir += 1
            yield from scantree(entry.path)
        else:
            #ignore file types not on include list
            if not any(entry.path.lower().endswith("."+inc.split('.')[-1]) for inc in vars.include_all):
                continue

            yield entry


def already_crawled(file:str) -> True:
    """
    Reads/creates list of files crawled by this program. Used to ignore future crawls if the file remains unmodified from previous crawl.
    :param file: str path of file to crawl
    """
    modified = os.path.getmtime(file)
    # print("SELECT * FROM crawled WHERE path="+file+" AND mod="+modified)
    exists= sl.select("SELECT rowid, mod FROM crawled WHERE path='"+file+"' LIMIT 1",
    fetchall=False)
    # if the filename matches and the modified date is unchanged

    if exists:
        if exists['mod'] == modified:
            set_active(exists['id'])
            return True
    #if file matches but has been since modified
        else:
            update = "UPDATE crawled SET mod = {} WHERE rowid={}".format(modified, exists['id'])
            sl.c.execute(update)
            vars.current_id = exists['id']
            sl.commit()
            set_active(exists['id'])
            return False
    # if new file create record
    newcrawled = (file, "None", modified, "None")
    sl.addRow('crawled (path, title, mod, list)', newcrawled)
    vars.current_id = sl.id()[0]
    sl.commit()
    return False


def crawl(haystack:str) -> None:
    """Creates an index for every significant word used in supplied file. Scores the word by how many times it is used. Tracks title score and modification date of file.
    :param haystack: str path to file
    """

    tic = time.perf_counter()
    modified = time.ctime(os.path.getmtime(haystack)) # when was the file last changed

    #sort which files to search inside and which to search file name only
    inc_list = vars.include_text

    # Is the file intended for text searching? Use html parser.
    if any(x in haystack for x in inc_list):
        try: #Just in case the file has data that can't be read
            with open(haystack, 'rb') as file:
                soup = BeautifulSoup(file, 'html.parser')
                content = str(soup.get_text()).lower() #reads text content
        except:
            print_red("Error in reading file content. Assigning search to title only.\n{}".format(haystack))
            content = os.path.splitext(os.path.basename(haystack))[0]
        try:
            title = soup.find('title').string.lower()
        except: # if file has no html title, treat file name as title
            title = os.path.splitext(os.path.basename(haystack))[0]
    else: # If file is not intended to be read, treat the title as extent of search
        content = title = os.path.splitext(os.path.basename(haystack))[0].lower()

    content = re.sub(r'[^a-zA-Z\s]+','',content).split() # creates list of words, stripped of nonletters
    s_title = re.sub(r'[^a-zA-Z\s]+','',title).split() # for searching title
    count_dict = {n:content.count(n) for n in set(content)} #creates a dict of words with their wordcount
    count_title = {n:s_title.count(n) for n in set(s_title)} # for hits in title

    content = list(set(content) - set(vars.exclude_words)) #creates list of valid words

    #list of valid words to catalogue generated the last time the file was crawled
    sel = "SELECT list FROM crawled WHERE rowid="+str(vars.current_id)
    old_data = sl.select(sel, fetchall=False)
    # print(old_data)

    if old_data[0] != "None":
        old_words = json.loads(old_data[0])
        removed_words = set(old_words)-set(content) #compares old words to incoming words
        purge_words(removed_words, vars.current_id) #delete occurences/words which are no longer in use
        new_words = list(content) #make copy of new words to catalogue for next comparison
        content = list(set(content)-set(old_words)) #minimize the number of words to catalogue: only new words
    else: # for first time through. the file_store.json doesn't exist yet
        new_words = content

    blob = json.dumps(new_words)
    update = "UPDATE crawled SET list=?, title='{}' WHERE rowid={}".format(title, vars.current_id)
    sl.c.execute(update, (blob,))
    sl.commit()

    fletter = {l[0] for l in content}
    for l in fletter:
        sl.makeFletter(l)
    for word in content:
        fl = word[0]
        word_score = count_dict[word]
        in_title = count_title[word] if word in count_title else 0
        data = (vars.current_id, word, word_score, in_title)
        sl.addRow(fl, data)
    sl.commit()
    # create new list of first letters used
    # fletter = {l[0] for l in content}
    # for l in fletter:
    #
    #     for word in content:
    #         # only append the words_list for words of same first letter
    #         if word[0] != l:
    #             continue
    #         word_score = count_dict[word]
    #         in_title = count_title[word] if word in count_title else 0
    #
    #
    #         new_data = {
    #
    #             "score":word_score,
    #             "in_title":in_title,
    #             "modified":modified
    #         }

        #optional logging, in case you were super interested
        # print("successfully scraped "+Color.B_White+Color.F_Black+word+Color.F_Default+Color.B_Default)


    vars.num_words += len(content)
    toc = time.perf_counter()
    print_green("Crawled {} in {:0.4f} seconds".format(haystack, toc-tic) )


def purge_words(removed:set, id:int) -> None:
    """
    Deletes words sent to it from the letter_store file.
    :param removed: a set of words to remove from record
    :param title: the title of the page to remove record from
    """

    #ignore empty requests
    if not removed:
        return

    for word in removed:
        #pull up the letter_store file of the word

        fl = str(word[0])
        Dele = "DELETE FROM {} WHERE word={} and id={}".format(fl, word, id)
        # print(Dele)
        sl.c.execute("DELETE FROM "+fl+" WHERE word=:word and id=:id", {'word':word,'id':id})

    sl.commit()
    vars.num_purge += len(removed)


def clear_active()->None:
    update = "UPDATE crawled SET active=0"
    sl.c.execute(update)
    sl.commit()


def set_active(id:int)->None:
    update = "UPDATE crawled SET active=1 WHERE rowid={}".format(id)
    sl.c.execute(update)
    sl.commit()


def del_inactive() -> None:
    deleted = sl.select("SELECT rowid, list FROM crawled WHERE active=0")
    for d in deleted:
        decoded = json.loads(d['list'])
        purge_words(decoded, d['id'])

    wipe = "DELETE FROM crawled WHERE active=0"
    sl.c.execute(wipe)
    sl.commit()
