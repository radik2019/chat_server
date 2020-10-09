import json


def add_data(name, passw):
    try:
        with open('db.json', 'r') as df:
            dct = json.load(df)
    except FileNotFoundError:
        dct = {}
    dct[name] = passw
    with open('db.json', 'w') as file:
        json.dump(dct, file)
    print(dct)


def user_exists(name, passw):
    with open('db.json', 'r') as df:
        dct = json.load(df)
    for user in dct:
        if (user == name) and (dct[user] == passw):
            return True
    return False


def remove_user(user):
    with open('db.json', 'r') as df:
        dct = json.load(df)
    try:
        del(dct[user])
        with open('db.json', 'w') as file:
            json.dump(dct, file)
        return f"the user '{user}' rimoved from database"
    except KeyError:
        return f"the user '{user}' does not exist"


add_data("cristiane", 63343)
print(user_exists("radu",123))
print(remove_user('masha'))
