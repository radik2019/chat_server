
import json
import socket
from threading import Thread
from sys import argv
from sys import exit
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect_to_server(soc):
    global s
    s.connect(soc)


def add_data(username, passw):

    dct = dict()
    dct["name"] = username
    dct["password"] = passw
    doc = json.dumps(dct)
    s.send(bytes(doc, encoding="utf-8"))
    risponse = s.recv(1024).decode()
    if risponse == '1':
        print("[ * ] welcome to the chat!")
        return doc
    else:
        print("[ ! ] wrong name or password!")
        sleep(1)
        exit()


def send_message():
    global s
    while True:
        if not s:
            s.close()
            return
        message = input()
        s.send(message.encode())


def receive_message():
    global s
    while True:
        if not s:
            s.close()
            return
        print(s.recv(1024).decode())


def get_loggin(username="none", user_password="none"):
    return [username, user_password]


if __name__ == "__main__":

    connect_to_server(("192.168.1.229", 6000))
    try:
        userdata = argv
        # userdata=[1, 'radu', '123w']
        name, password = get_loggin(userdata[1], userdata[2])
    except IndexError:
        name, password = get_loggin()

    add_data(name, password)

    t1 = Thread(target=receive_message)
    t2 = Thread(target=send_message)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
