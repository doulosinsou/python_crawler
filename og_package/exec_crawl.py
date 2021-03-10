from search_functions.crawl import *
# global num_files, num_dir, num_words, num_purge


#begin calling code and time it
date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print(date)

start_timer = time.perf_counter()
search_dir = vars.my_path
print_red(search_dir)
call_files(search_dir) #this starts it all
end_timer = time.perf_counter()
total_time = end_timer-start_timer

print()
print("Report: ")
print_green("Indexed {} words".format(vars.num_words))
for type in vars.num_type:
    print_yellow("\t{}: {}".format(type, vars.num_type[type]))
print()
print_yellow("Purged {} files".format(vars.num_purge))
# print_yellow("Report: {} files from {} directories.\nIndexed {} words.\nPurged {} words".format(vars.num_files, vars.num_dir, vars.num_words, vars.num_purge))
print_green("Total time: {:0.4}s".format(total_time))

endfile = " end file ".center(80, "*")
print(endfile, "\n")
