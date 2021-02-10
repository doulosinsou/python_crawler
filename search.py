def search_for(needle:str, haystack:str):
    """
    prints number of matches for needle in haystack

    :param needle: string to search for
    :param haystack: stringed path of html file to search in
    """
    from bs4 import BeautifulSoup
    import string
    needle = str(needle).lower() # .center(len(needle)+2, ' ')
    haystack = str(haystack)
    exclude_words = list(open('exclude_words.txt').read().splitlines())
    with open(haystack, 'rb') as file:
        soup = BeautifulSoup(file, 'html.parser')
        content = str(soup.get_text()).lower()
        man_count = 0;
        for word in content.split():
            tomatch = word.translate(str.maketrans('', '', string.punctuation))
            if (needle == tomatch) and (needle not in exclude_words):
                man_count += 1
        print("'{}' occured {} times in this file".format(needle, man_count))


while True:
    needle = input("search for term: ")
    if needle == "quit":
        break
    search_for(needle, 'test_files/commitment.htm')
