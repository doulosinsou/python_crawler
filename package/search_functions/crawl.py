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
# from search_functions.vars import *

def call_files(dir="./test_files") -> None:
    """
    Compiles each file in directory. Sends to `crawl()` for parsing.
    :param dir: str of relative directory to search
    """
    # global vars.num_files
    for files in scantree(dir):
        #to ignore unnecessary repeats
        if already_crawled(files.path):
            print(files.path+" already crawled")
            continue
        vars.num_files += 1
        crawl(files.path)
        # return


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
    modified = str(os.path.getmtime(file))
    with open(vars.crawled) as cfiles:
        flist = json.load(cfiles)
    for f in flist:
        fsplit = f.split('_MOD_')
        path = fsplit[0]
        mod = fsplit[1]
        # if the filename matches and the modified date is unchanged
        if (path == file) and (mod == modified):
            return True
    # if new file or if file has been since modified, create record
    flist.append(file+"_MOD_"+modified)
    with open(vars.crawled, 'w') as cfiles:
        json.dump(flist, cfiles, indent=4, sort_keys=True)
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
    file_store = vars.index_path+'/path_store/'+os.path.splitext(os.path.basename(haystack))[0]+'_store.json'
    try:
        with open(file_store, "r") as fstore:
            old_words = json.load(fstore)
        removed_words = set(old_words)-set(content) #compares old words to incoming words
        purge_words(removed_words, title) #delete occurences/words which are no longer in use
        new_words = list(content) #make copy of new words to catalogue for next comparison
        content = list(set(content)-set(old_words)) #minimize the number of words to catalogue: only new words
    except: # for first time through. the file_store.json doesn't exist yet
        new_words = content

    with open(file_store, 'w') as fstore: #create or overwrite file_store for list (set) of words to search
        json.dump(new_words, fstore)

    # create new list of first letters used
    fletter = {l[0] for l in content}
    for l in fletter:

        if vars.sql_database:
            functions.create(l)
            sql_list = []
        if vars.local_database:
            # find/create LOCAL letter_store
            store_file = vars.index_path+"/{}_store.json".format(l)
            if os.path.exists(store_file) == False:
                with open(store_file, "w") as store_data:
                    empty = {}
                    json.dump(empty, store_data)

            # get existing data from LOCAL letter store
            with open(store_file) as store_data:
                words_list = json.load(store_data)

        if not vars.sql_database and not vars.local_database:
            print("No database is enabled. Chack the .config file and enable either sql or local storage")
            return

        for word in content:
            # only append the words_list for words of same first letter
            if word[0] != l:
                continue
            word_score = count_dict[word]
            in_title = count_title[word] if word in count_title else 0

            #add new data to array of word in word_store
            if vars.sql_database:
                new_data = (word, title, haystack, word_score, in_title, modified)
                # sql uses list of tuples
                sql_list.append(new_data)

            if vars.local_database:
                #if the word doesn't exist in LOCAL store (yet), make blank list
                if word not in words_list:
                    words_list[word] = []

                new_data = {
                    "word":word,
                    "title":title,
                    "file_path":haystack,
                    "score":word_score,
                    "in_title":in_title,
                    "modified":modified
                }
                words_list[word].append(new_data)

        if vars.sql_database:
            unpacked = ", ".join(map(str,sql_list))
            functions.postit(l, unpacked)


        if vars.local_database:
            with open(store_file,'w') as stuff:
                 json.dump(words_list, stuff, indent=4, sort_keys=True)

        #optional logging, in case you were super interested
        # print("successfully scraped "+Color.B_White+Color.F_Black+word+Color.F_Default+Color.B_Default)
    vars.num_words += len(content)
    toc = time.perf_counter()
    print_green("Crawled {} in {:0.4f} seconds".format(haystack, toc-tic) )


def purge_words(removed:set, title:str) -> None:
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
        first_letter = str(word[0])
        store_file = "index/{}_store.json".format(first_letter)
        with open(store_file) as stuff:
            tokeep = json.load(stuff)

        #remove occurence of word if file title matches
        for key, occ in enumerate(tokeep[word]):
            # print(occ)
            if occ['title'] == title:
                del tokeep[word][key]
        #if the word now has no more occurences, remove
        del_words = []
        if len(tokeep[word]) == 0:
            del_words.append(word)
        for d in del_words:
            del tokeep[d]
        with open(store_file,'w') as stuff:
            json.dump(tokeep, stuff, indent=4, sort_keys=True)
    vars.num_purge += len(removed)
