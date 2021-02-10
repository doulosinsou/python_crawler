import os

from bs4 import BeautifulSoup
import string
import json


def crawl(haystack:str) -> None:
    """Creates an index for every significant word used in supplied file. Scores the word by how many times it is used plus if it occurs in title of html.
    Dependencies{
    string,
    json,
    BeautifulSoup,
    os,
    exclude_word (local),
    }

    """
    print("about to crawl: "+haystack)
    haystack = str(haystack)
    exclude_words = list(open('exclude_words.txt').read().splitlines())
    with open(haystack, 'rb') as file:
        soup = BeautifulSoup(file, 'html.parser')
        content = str(soup.get_text()).lower()

        title = soup.find('title').string.lower()

        for word in content.split():
            word = word.translate(str.maketrans('', '', string.punctuation))
            if exclude_word(word) == False:
                continue
            word_score = count_words(word, content.split())
            word_score += count_words(word, [title])*40

            first_letter = str(word[0])

            dump_file = "index/{}_dump.json".format(first_letter)
            if os.path.exists(dump_file) == False:
                f = open(dump_file, 'w')
                baseline = {}
                f.write(json.dumps(baseline))
                f.close()

            with open(dump_file) as dump_data:
                words_list = json.load(dump_data)

                new_data = {
                    "title":str(title),
                    "file_path":haystack,
                    "score":word_score
                }

                if word not in words_list:
                    words_list[word] =[]

                exists = 0
                for item in words_list[word]:
                    for value in item.values():
                        if title == value:
                            exists += 1
                if exists:
                    continue
                words_list[word].append(new_data)
                print(words_list)

            if exists:
                continue
            with open(dump_file,'w') as stuff:
                 json.dump(words_list, stuff, indent=4, sort_keys=True)

            print("successfully scraped "+word)
    print("completed")


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
        if file.lower().endswith(inc):
            # print("{} returns false".format(file))
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


def exclude_path(file:str) -> False:
    type = "exclude_path.txt"

    """return False if supplied path matches any line in exclusion file"""
    exclude_path = list(open(type).read().splitlines())
    for ex in exclude_path:
        if ex in file: ## must be in to match part of path rather than all of it
            return False
    return True


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
        if exclude_path(entry.path) == False:
            continue
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            if include_file_type(entry.path):
                continue
            yield entry


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

        crawl(local_path)


call_files('./test_files/demo')
