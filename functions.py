list_content = "The moon shown red on night one night one night the moon shown red"
list_list = list_content.lower().split()
list_sorted = list_list.sort()

print(list_list)

for word in set(list_list):
    count = list_list.count(word)
    print("count of {} is {}".format(word, count))
