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

print_yellow("Crawled {} files from {} directories.\nIndexed {} words.\nPurged {} words".format(vars.num_files, vars.num_dir, vars.num_words, vars.num_purge))
print_green("Total time: {:0.4}s".format(total_time))

endfile = " end file ".center(80, "*")
print(endfile, "\n")

if vars.sql_database:
    print("Would you like to post this data to your mysql database at this time? (it may take a few minutes)")
    print("type 'yes' or 'no' : ")
    confirm_sql = input()
    if str(confirm_sql.lower()) == 'yes':
        import subprocess
        file = functions.pathit('test.py')
        exec(open("search_functions/test.py").read())
        # subprocess.run('search_functions/test.py', shell=True)
        # os.execl('search_functions/test.py', "njlnj")
        print("End of mysql process")
    else:
        print('No sql at this time')
