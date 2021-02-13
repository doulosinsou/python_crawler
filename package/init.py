from search_functions.crawl import *
# global num_files, num_dir, num_words, num_purge


#begin calling code and time it
date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print(date)
# search_dir = open(vars.my_path, 'r').read().strip()
search_dir = vars.my_path
# search_dir = os.path.join(os.path.dirname((os.path.abspath(__file__))))+"/test_files"
# print_red(search_dir)

start_timer = time.perf_counter()
call_files(search_dir) #this starts it all
end_timer = time.perf_counter()
total_time = end_timer-start_timer

print_yellow("Crawled {} files from {} directories.\nIndexed {} words.\nPurged {} words".format(vars.num_files, vars.num_dir, vars.num_words, vars.num_purge))
print_green("Total time: {:0.4}s".format(total_time))

endfile = " end file ".center(80, "*")
print(endfile, "\n")
