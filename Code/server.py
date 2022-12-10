import json
import socket
from _thread import *

host = "127.0.0.1"
port = 8080
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = []


def client_handler(connection):

    while True:
        # connection.send("Hello".encode())
        for c in clients:
            c.sendall("sajjad".encode())
        data = connection.recv(1024).decode()
        # connection.sendall("question".encode())  # send data to the client

        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))

        # server_q = input()
        # connection.sendall(data)





    connection.close()


try:
    server_socket.bind((host, port))
except socket.error as e:
    print(str(e))

print(f'Server is listing on the port {port}...')
server_socket.listen(2)

while True:

    client, address = server_socket.accept()
    clients.append(client)
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(client_handler, (client,))
