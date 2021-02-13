with open('exclude_words.txt') as excludes:
    excludes = set(excludes.read().splitlines())
excludes = list(excludes)
excludes.sort()
excludes = '\n'.join(excludes)
with open('exclude_words.txt', 'w') as new:
    new.write(excludes)

with open('exclude_words.txt') as nowsorted:
    print(nowsorted.read())
