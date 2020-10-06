
import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("192.168.1.229", 6000))

list_of_sockets = []
server_socket.listen()
server_socket.setblocking(False)
print("server is running!!!")


def add_socket():
	global list_of_sockets
	while True:
		# print("while loop...")
		server_socket.setblocking(False)
		try:
			client, addr = server_socket.accept()
			list_of_sockets.append(client)
			print("connection from", addr)
		except BlockingIOError:
			continue




def read_socket():
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
						print(i,request.decode())
						s = "connected  ".encode()
						list_of_sockets[i].send(s)
						print("number of connection = ", len(list_of_sockets))
						# list_of_sockets[i].close()
						continue
				except BlockingIOError:
					continue

			except OSError:
				list_of_sockets.remove(list_of_sockets[i])
				break



t1 = threading.Thread(target=add_socket)
t2 = threading.Thread(target=read_socket)
t1.start()
t2.start()

t1.join()

t2.join()
