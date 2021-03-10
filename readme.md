#Python Crawler by Moyer Audio
Search and catalogue words from files in directories

##Install
Unpack zip onto Python 3 enabled directory

Install BeautifulSoup4 (tested with version 4.9.3)
`pip install beautifulsoup4`

Uses imports:
```
os
re
string
json
time
sqlite3
ConfigParser

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
Run `exec_crawl.py` to scrape words from directory and build store files.

##Wipe
Re-running `exec_crawl.py` checks the modified date of each file. Run `wipe.py` to clear store files AND log file.

##Use
The store files are sqlite `crawled.db`. There are two table structures represented below:

```
TABLE crawled
cols:
(id int primary [alias of rowid], path text,  title text, mod[idfied date] int, list [of previously crawled words written as json] blob)

TABLE [alphabet letter]
cols:
(id [uses rowid of path] int, word text, count int, in_title int)

```

To use the database, call a join method like below:

```
SELECT word, title, count, in_title
FROM _letter_
INNER JOIN crawled on crawled.rowid = _letter_.id
WHERE word='_search_word_'
```
