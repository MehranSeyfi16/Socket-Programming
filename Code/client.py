import socket

HOST = "127.0.0.1"
PORT = 8080
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))
except socket.error as e:
    print(str(e))

while True:
    data = client_socket.recv(1024).decode()  # receive response
    print(data)
    data = ""
    Input = input('Your message: ')
    client_socket.send(str.encode(Input))

client_socket.close()