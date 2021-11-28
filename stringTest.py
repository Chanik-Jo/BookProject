def insert_dash(string, index):
    return string[:index] + '-' + string[index:]

string ="9788963010793"
print(string)


def turnStringToIsbn(string):
    string = insert_dash(string, 3)
    string = insert_dash(string, 6)
    string = insert_dash(string, 11)
    string = insert_dash(string, 15)
    print(string)
    return string