
#!/usr/bin/python3

import socket
import threading
from data_IO import *
import os
import hashlib


def getNetworkIp():
    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s2.connect(('<broadcast>', 0))
    return s2.getsockname()[0]

ip_address = getNetworkIp()
port = 6000
print(ip_address)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((ip_address, port))

numb_connect = 0
list_of_sockets = []
users_list = []
server_socket.listen()
server_socket.setblocking(False)
print("server is running!!!")

"""
add_data(name, passw)
user_exists(name, passw)
remove_user(user)
"""

def add_socket():
    global numb_connect
    global list_of_sockets
    while True:

        server_socket.setblocking(False)
        try:
            client, addr = server_socket.accept()

            def riceve_json_data(data):

                try:
                    with open("riceved_data.json", "wb") as fl:
                        fl.write(data)
                    with open("riceved_data.json") as df:
                        client_data = json.load(df)

                        return client_data

                except FileNotFoundError:
                    pass

            r = client.recv(1024)
            name = str()

            client_data = riceve_json_data(r)
            name2 = client_data["name"]
            passwd = client_data["password"]

            # name = client.recv(1024).decode()[:-1] + ":: "
            # client.send("password :  ".encode())
            # passwd = client.recv(1024).decode()[:-1]
            if user_exists(name2, passwd):
                name = name2
                os.remove("riceved_data.json")
                print("json file is removed!!!")

                list_of_sockets.append(client)

                users_list.append(name)
                print(f"{name} is connected")
                if numb_connect != len(list_of_sockets):
                    print("number of connection = ", len(list_of_sockets))
                    print(users_list)
                    numb_connect = len(list_of_sockets)
            else:
                client.close()
                continue
        except BlockingIOError:
            continue

def read_socket():
    # numb_connect = 0
    global numb_connect
    global list_of_sockets
    while True:
        for i in range(len(list_of_sockets)):
            try:
                list_of_sockets[i].setblocking(False)
                try:
                    request = list_of_sockets[i].recv(1024)
                    if not request:
                        list_of_sockets[i].close()
                    else:
                        for k in range(len(list_of_sockets)):
                            if list_of_sockets[i] == list_of_sockets[k]:
                                pass
                            else:
                                message = (users_list[i] + ": " + request.decode()).encode()
                                list_of_sockets[k].send(message)
                                # list_of_sockets[k].send(request)
                        if numb_connect != len(list_of_sockets):
                            print("number of connection = ", len(list_of_sockets))
                            print(users_list)
                            numb_connect = len(list_of_sockets)
                        # list_of_sockets[i].close()
                        continue
                except BlockingIOError:
                    continue

            except OSError:
                print(f"{users_list[i]} is quiting..")

                list_of_sockets.remove(list_of_sockets[i])
                users_list.remove(users_list[i])
                if numb_connect != len(list_of_sockets):
                    print("number of connection = ", len(list_of_sockets))
                    print(users_list)
                    numb_connect = len(list_of_sockets)                
                break


t1 = threading.Thread(target=add_socket)
t2 = threading.Thread(target=read_socket)
t1.start()
t2.start()
t1.join()
t2.join()


