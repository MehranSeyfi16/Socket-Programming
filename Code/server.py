import json
import socket
import threading
import time

host = "127.0.0.1"
port = 8080
#scores = {"playerA": 0, "playerB": 0, "playerC": 0}
clientCount = 0

with open('questions.json', 'r') as myFile:
    questions = json.load(myFile)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")



    for i in range(len(questions)):
        data = f'question{i+1} is: {questions[i]["question"]}\noptions are: {questions[i]["options"]}'
        conn.sendall(str.encode(data))

        ans = conn.recv(1024).decode('utf-8')
        print(ans)
        # print(conn.getpeername()[1])
        # if ans == str(questions[i]["answer"]):
        #     pass


print('[STARTING] Server is starting...')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind((host, port))
except socket.error as e:
    print(str(e))

server_socket.listen()
print(f'[LISTENING] Server is listing on {host}:{port}')

while True:
    conn, addr = server_socket.accept()
    clientCount += 1
    threading.Thread(target=handle_client, args=(conn, addr)).start()
    print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')
