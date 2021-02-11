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

Example: The following does not crawl files in the folders:
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
Open `include.txt` . Write dot + extention of files you want to crawl on new line. Prepend crawlable files with 'TEXT'. This tells the program to read the information inside.
Example:
```
TEXT.htm
TEXT.html
TEXT.php
.mp3
```
__note: non TEXT prepended files only catalogue its own title__
listen_to_jazz.mp3 will scrape the words 'listen', 'to', 'jazz'.

###Exclude common words
Update `exclude_words.txt` for specific words you want to not scrape.

##Run
Run `crawl.py` from command line to scrape words from directory and build dump files.

##Wipe
Re-running `crawl.py` will only add words if the word does not have that file associated with it. Therefore updating the file will not inherently add new occurrences or scores. Run `wipe_index.py` from command line to clear dump files.

##Use
The dump files are .json and can be called as such. The 'score' of the word is used to calculate the number of times the word is used in the file.
