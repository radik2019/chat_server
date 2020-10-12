import json
import hashlib

def hashing_pass(s):
    s = bytes(s, encoding="utf-8")
    return hashlib.sha256(s).hexdigest()


def add_data(name, passw):
    try:
        with open('db.json', 'r') as df:
            dct = json.load(df)
    except FileNotFoundError:
        dct = {}
    dct[name] = hashing_pass(passw)
    with open('db.json', 'w') as file:
        json.dump(dct, file)
    print(dct)


def user_exists(name, passw):
    with open('db.json', 'r') as df:
        dct = json.load(df)
    for user in dct:
        if (user == name) and (dct[user] == hashing_pass(passw)):
            print("Welcome!")
            return True
    print("name or password error")
    return False

"""
add_data(name, passw)
user_exists(name, passw)
remove_user(user)
"""



def remove_user(user):
    with open('db.json', 'r') as df:
        dct = json.load(df)
    try:
        del(dct[user])
        with open('db.json', 'w') as file:
            json.dump(dct, file)
        return f"the user '{user}' removed from database"
    except KeyError:
        return f"the user '{user}' does not exist"

if __name__ == "__main__":
    add_data('radu','123')
    print(user_exists("radu","123"))
    print(remove_user('masha'))
