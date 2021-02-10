import re

content = "abcdefg...12345,: _'hijklmnop-67890"

regex = re.compile(r'[^a-zA-Z\s]')
content = regex.sub('',content)

print(content)
