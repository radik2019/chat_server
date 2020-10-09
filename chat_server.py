
#!/usr/bin/python3

import socket
import threading



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
address_list = []
server_socket.listen()
server_socket.setblocking(False)
print("server is running!!!")


def add_socket():
    global numb_connect
    global list_of_sockets
    while True:
        # print("while loop...")
        server_socket.setblocking(False)
        try:
            client, addr = server_socket.accept()
            client.send("id:  ".encode())
            name = client.recv(1024).decode()[:-1] + ":: "

            list_of_sockets.append(client)

            address_list.append(name)
            print(f"{name} is connected")
            if numb_connect != len(list_of_sockets):
                print("number of connection = ", len(list_of_sockets))
                print(address_list)
                numb_connect = len(list_of_sockets)
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
                                # request = f"{address_list[i]}:: {request.decode()}".encode()
                                list_of_sockets[k].send(address_list[i].encode())
                                list_of_sockets[k].send(request)
                        if numb_connect != len(list_of_sockets):
                            print("number of connection = ", len(list_of_sockets))
                            print(address_list)
                            numb_connect = len(list_of_sockets)
                        # list_of_sockets[i].close()
                        continue
                except BlockingIOError:
                    continue

            except OSError:
                print(f"{address_list[i][:-3]} is quiting..")


                list_of_sockets.remove(list_of_sockets[i])
                address_list.remove(address_list[i])
                if numb_connect != len(list_of_sockets):
                    print("number of connection = ", len(list_of_sockets))
                    print(address_list)
                    numb_connect = len(list_of_sockets)                
                break


t1 = threading.Thread(target=add_socket)
t2 = threading.Thread(target=read_socket)
t1.start()
t2.start()
t1.join()
t2.join()


