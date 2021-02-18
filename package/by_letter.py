my_dict = {
    'a': [{
        'adam': "apple",
        'admiral': "akbar"
    },
        {
        'agent': 'able',
        'argument': 'amplify'
    }
    ],
    'b': [{
        'barry': 'banana',
        'blury': 'binks'
    },
        {
        'babyface': 'brow',
        'blue': 'bonnet'
    }
    ]
}



more = {'a':[{'colonel':'crumpet'}]}
my_dict.update(my_dict.get('a', more))

print(my_dict)
