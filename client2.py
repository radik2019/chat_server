
import json
import socket
from threading import Thread
from sys import argv



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server(soc):
    global s
    s.connect(soc)


def add_data(name, passw):

    dct = {}
    dct["name"] = name
    dct["password"] = passw
    print(1,dct)
    doc = json.dumps(dct)
    print(2,doc)
    s.send(bytes(doc, encoding="utf-8"))
    return doc


def send_message():
    global s
    while True:
        message = input()
        s.send(message.encode())


def receive_message():
    global s
    while True:
        print(s.recv(1024).decode())

def get_loggin(name="none", password="none"):
    return [name, password]


if __name__ == "__main__":

    connect_to_server(("192.168.1.229", 6000))
    try:
        userdata = argv
        name, password = get_loggin(userdata[1],userdata[2])
    except IndexError:
        name, password = get_loggin()


    add_data(name, password)

    t1 = Thread(target=receive_message)
    t2 = Thread(target=send_message)
    t1.start()
    t2.start()
    t1.join()
    t2.join()