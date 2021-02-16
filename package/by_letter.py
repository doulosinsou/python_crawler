words = ['ascend', 'apples', 'elephant', 'banana', 'bone', 'zebras', 'zoo']
fletter = {l[0] for l in words}

for l in fletter:
    group=[]
    for w in words:
        if w[0] == l:
            group.append(w)
    print(group)
