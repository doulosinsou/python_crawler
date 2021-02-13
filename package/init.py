from search_functions.crawl import *
# global num_files, num_dir, num_words, num_purge


#begin calling code and time it
date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print(date)

start_timer = time.perf_counter()
search_dir = vars.my_path
call_files(search_dir) #this starts it all
end_timer = time.perf_counter()
total_time = end_timer-start_timer

print_yellow("Crawled {} files from {} directories.\nIndexed {} words.\nPurged {} words".format(vars.num_files, vars.num_dir, vars.num_words, vars.num_purge))
print_green("Total time: {:0.4}s".format(total_time))

endfile = " end file ".center(80, "*")
print(endfile, "\n")
