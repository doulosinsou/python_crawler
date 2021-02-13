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
num_purge = 0

def call_files(dir="./test_files") -> None:
    """
    Compiles each file in directory. Sends to `crawl()` for parsing.
    :param dir: str of relative directory to search
    """
    global num_files
    for files in scantree(dir):
        rel_file = os.path.relpath(files.path, dir)
        local_path = "{}/{}".format(dir,rel_file)
        #to ignore unnecessary repeats
        if already_crawled(local_path):
            print(local_path+" already crawled")
            continue
        num_files += 1
        crawl(local_path)


def scantree(path:str) -> dict:
    """
    Recursively yield DirEntry objects for given directory.
    :param path: str local directory to search
    :return: obj with data about the files, namely: file path
    """

    global num_dir
    exclude_path = list(open('exclude_path.txt').read().splitlines())
    include_path = list(open("include.txt").read().splitlines())

    for entry in os.scandir(path):
        #ignore paths/files on exclude list
        if any(ex in entry.path for ex in exclude_path):
            continue
        #recurse through directories
        if entry.is_dir(follow_symlinks=False):
            num_dir += 1
            yield from scantree(entry.path)
        else:
            #ignore file types not on include list
            if not any(entry.path.lower().endswith("."+inc.split('.')[-1]) for inc in include_path):
                continue
            yield entry


def already_crawled(file:str) -> True:
    """
    Reads/creates list of files crawled by this program. Used to ignore future crawls if the file remains unmodified from previous crawl.
    :param file: str path of file to crawl
    """
    modified = str(os.path.getmtime(file))
    crawled = './index/crawled.json'
    with open(crawled) as cfiles:
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
    with open(crawled, 'w') as cfiles:
        json.dump(flist, cfiles, indent=4, sort_keys=True)
    return False


def crawl(haystack:str) -> None:
    """Creates an index for every significant word used in supplied file. Scores the word by how many times it is used. Tracks title score and modification date of file.
    :param haystack: str path to file
    """
    global num_words #to count how many words are processed
    tic = time.perf_counter()
    modified = time.ctime(os.path.getmtime(haystack)) # when was the file last changed

    #sort which files to search inside and which to search file name only
    with open('include.txt', 'r') as includes:
        text_files = includes.read().lower().splitlines()
        file_stop = [k for k, n in enumerate(text_files) if n == "non-text:"]
    inc_list = [w for w in text_files[1:file_stop[0]] if w]

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
        content = title = os.path.splitext(os.path.basename(haystack))[0]

    content = re.sub(r'[^a-zA-Z\s]+','',content).split() # creates list of words, stripped of nonletters
    s_title = re.sub(r'[^a-zA-Z\s]+','',title).split() # for searching title
    count_dict = {n:content.count(n) for n in set(content)} #creates a dict of words with their wordcount
    count_title = {n:s_title.count(n) for n in set(s_title)} # for hits in title

    exclude_path = list(open('exclude_words.txt').read().splitlines())
    content = list(set(content) - set(exclude_path)) #creates list of valid words

    #list of valid words to catalogue generated the last time the file was crawled
    file_store = './index/path_store/'+os.path.splitext(os.path.basename(haystack))[0]+'_store.json'
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

    for word in content:
        word_score = count_dict[word]
        in_title = count_title[word] if word in count_title else 0

        # find/create letter_store
        first_letter = str(word[0])
        store_file = "index/{}_store.json".format(first_letter)
        if os.path.exists(store_file) == False:
            with open(store_file, "w") as store_data:
                empty = {}
                json.dump(empty, store_data)

        with open(store_file) as store_data:
            words_list = json.load(store_data)

        #if the word doesn't exist in store (yet), make blank list
        if word not in words_list:
            words_list[word] = []

        new_data = {
            "title":title,
            "file_path":haystack,
            "score":word_score,
            "in_title":in_title,
            "modified":modified
        }

        #add new data to array of word in word_store
        words_list[word].append(new_data)

        with open(store_file,'w') as stuff:
             json.dump(words_list, stuff, indent=4, sort_keys=True)

        #optional logging, in case you were super interested
        # print("successfully scraped "+Color.B_White+Color.F_Black+word+Color.F_Default+Color.B_Default)
    num_words += len(content)
    toc = time.perf_counter()
    print_green("Crawled {} in {:0.4f} seconds".format(haystack, toc-tic) )


def purge_words(removed:set, title:str) -> None:
    """
    Deletes words sent to it from the letter_store file.
    :param removed: a set of words to remove from record
    :param title: the title of the page to remove record from
    """
    global num_purge
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
    num_purge += len(removed)

#**********************************************************
#begin calling code and time it
date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print(date)
search_dir = open('my_path.txt', 'r').read().strip()

start_timer = time.perf_counter()
call_files(search_dir) #this starts it all
end_timer = time.perf_counter()
total_time = end_timer-start_timer

print_yellow("Crawled {} files from {} directories.\nIndexed {} words.\nPurged {} words".format(num_files, num_dir, num_words, num_purge))
print_green("Total time: {:0.4}s".format(total_time))

endfile = " end file ".center(80, "*")
print(endfile, "\n")
