import json

z = {}
y = json.dumps(z)
dict = json.loads(y)


dict = {}

mydict = {'new':'unique', "other":'other key'}

if 'new' not in dict:
    dict['new'] = []

myword = dict['new']
myword.append(mydict)
dict['new'] = myword

my2dict = mydict

exists = 0
for item in dict['new']:
    for value in item.values():
        print(value)
        if 'unique' in value:
            print('its not here')
            exists += 1
if not exists:
    dict['new'].append(my2dict)


print(dict)
