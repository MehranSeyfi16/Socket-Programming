import socket

host = "127.0.0.1"
port = 8080
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # client_socket.bind((host, 8081))
    client_socket.connect((host, port))
except socket.error as e:
    print(str(e))

print(f"[CONNECTED] Client connected to server at {host}:{port}")

connected = True
while connected:
    data = client_socket.recv(1024)
    print(data.decode('utf-8'))
    answer = input('write your answer: ')
    client_socket.send(str.encode(answer))
