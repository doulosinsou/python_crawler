#Python Crawler by Moyer Audio
Search and catalogue words from files in directories

##Install
Unpack zip onto Python 3 enabled directory

Install BeautifulSoup4 (tested with version 4.9.3)
`pip install beautifulsoup4`


###Update directory to search
Open `my_path.txt` . Enter relative or absolute path of directory to search. (Use `./` for relative path)

###Exclude certain files/folders
Open `exclude_path.txt` . Write folders, file names, or openings of file/folder names you wish to exclude from the crawl.

Example: The following does not crawl these files:
./my_path/subdir/myfile.txt
./my_path/skip_me.htm
./my_path/_oldData/
./my_path/_alsoskipped.htm

```
/subdir/
skip_me.htm
/_
```
###Include file types you want to crawl
Open `include.txt` . Two sections in the files are: 'Text:' and 'Non-text:'. Write dot + extension of files you want to crawl on new line in 'Text' section.

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
Update `exclude_words.txt` for specific words you want to not scrape.

##Run
Run `crawl.py` from command line to scrape words from directory and build dump files.

##Wipe
Re-running `crawl.py` checks the modified date of each file. Run `wipe_index.py` from command line to clear dump files AND log file.

##Use
The dump files are .json and can be called as such. The 'score' of the word is the number of times the word is used in the file. If you wish to boost the score of matches in the Title, use the 'in-title' key. 'in-title' is the number of times the word is in the title.
