list_content = "The moon shown red on night one night one night the moon shown red"
list_list = list_content.lower().split()
list_sorted = list_list.sort()

print(list_list)

count_dict = {}
for word in set(list_list):
    count = list_list.count(word)
    # print("count of {} is {}".format(word, count))
    count_dict[word] = count
print(count_dict)



# with open('include.txt', 'r') as includes:
#     text_files = includes.read().lower().splitlines()
#     file_stop = [k for k, n in enumerate(text_files) if n == "non-text:"]
#     # for k, n in enumerate(text_files):
#     #     if n == ""
#
# valid_text = [w for w in text_files[1:file_stop[0]] if w]
# print("non-text occurs on line: {}".format(file_stop[0]))
# print(valid_text)
