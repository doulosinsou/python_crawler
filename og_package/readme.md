#Python Crawler by Moyer Audio
Search and catalogue words from files in directories

##Install
Unpack zip onto Python 3 enabled directory

Install BeautifulSoup4 (tested with version 4.9.3)
`pip install beautifulsoup4`

Uses imports:
```
import os
import re
import string
import json
import time
```

###Update directory to search
Open `.config`. Use `[location]`. Enter absolute path of directory to search in `search_abs` or relative path in `search_rel`. (Do not prepend `/` on relative path.)

###Exclude certain files/folders
Open `.config` . Use `[exclude]`. In `paths=` Write folders or openings of folder names you wish to exclude from the crawl. In `files=` write the files or openings of file names you wish to exclude.

Example: The following does not crawl these files:
./my_path/subdir/myfile.txt
./my_path/skip_me.htm
./my_path/_oldData/
./my_path/_alsoskipped.htm

```
path=
  /subdir/
  /_
file=
  skip_me.htm
```

###Include file types you want to crawl
Open `.config`. Use `[include]`. Two sections in the files are: 'Text:' and 'Non-text:'. Write dot + extension of files you want to crawl on new line in 'Text' section. All other file types you add to 'non-text' will use only the title of the file as it's search.

Example:
```
Text:
.htm
.html
.php

Non-text:
.mp3
```
__note: Non-text files only catalogue its own title__
The file `listen_to_jazz.mp3` will scrape the words 'listen', 'to', 'jazz'.

###Exclude common words
Update `/search_functions/exclude_words.txt` for specific words you want to not scrape. If you want to resort the list or purge duplicates, run `sort_ex_words.py`.

##Run
Run `crawl.py` to scrape words from directory and build store files.

##Wipe
Re-running `crawl.py` checks the modified date of each file. Run `wipe_index.py` to clear store files AND log file.

##Use
The store files are `.json` and can be read as javascript objects. Each object key is a word. It's value is a list of objects, each representing a file the word exists on. The 'score' of the word is the number of times the word is used in the file. If you wish to boost the score of matches in the Title, use the 'in-title' key. 'in-title' is the number of times the word is in the title.

```
s_store.json
{
  'searched_word':  [
                      {
                        "title":title of file,
                        "file_path":local/or/abs/path,
                        "score":1,
                        "in_title":0,
                        "modified":date-file-modified
                      }
                    ]
}

```
