import os
import json

dir = os.getcwd()+"/index"
for f in os.listdir(dir):
    if 'crawled.json' in f:
        path = dir+"/"+f
        with open(path,'r') as crawled:
            old = json.load(crawled)
        with open(path,'w') as crawled:
            blank = []
            json.dump(blank, crawled)
        continue
    print("Removing {}".format(f))
    os.remove(os.path.join(dir, f))
    if not os.path.isfile(os.path.join(dir, f)):
        print("successful")

log = open('logfile.log', 'w').close()
