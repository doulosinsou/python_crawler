import os
import re
import json
import time
from bs4 import BeautifulSoup

def exists(word, file):
    with open(file, 'rb') as doc:
        soup = BeautifulSoup(doc, 'html.parser')

        content = str(soup.get_text()).lower()
        content = re.sub(r'[^a-zA-Z\s]+','',content)

    for search in content.split():
        if word == search:
            return True
    return False


start_timer = time.perf_counter()
print('Beginnig word perge. Scanning for any words that no longer exist. This may take a few minutes.')
del_word_count = 0
del_occ_count = 0
for files in os.scandir('./index'):
    if 'crawled.json' in files.path:
        continue
    print('Scanning: '+files.path)
    with open(files.path, 'r') as z_dump:
        wlist = json.load(z_dump)
    del_words =[]
    for word, occlist in wlist.items():
        for ind, occ in enumerate(occlist):
            path = occ['file_path']
            in_it = exists(word, path)
            if not in_it:
                del wlist[word][ind]
                del_occ_count += 1
        if len(wlist[word]) == 0:
            print(word+' has no occs')
            del_words.append(word)
            del_word_count += 1
    for d in del_words:
        del wlist[d]
    with open(files.path, 'w') as z_dump:
        json.dump(wlist, z_dump, indent=4, sort_keys=True)

end_timer = time.perf_counter()
total_time = end_timer-start_timer

print("Deleted {} empty occurences and {} words in {:0.4}s".format(del_occ_count, del_word_count, total_time))
