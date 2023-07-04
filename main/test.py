a = {
    'subs' : [
        {
            'id' : '1',
            'name' : 'a'
        },
        {
            'id' : '2',
            'name' : 'b'
        },
        {
            'id' : '3',
            'name' : 'c'
        },
        {
            'id' : '4',
            'name' : 'd'
        },
    ]
}

for row in a['subs']:
    print(row['id'])