import json
import socket
import threading
import time

host = "127.0.0.1"
port = 8080
clientCount = 0
CLIENTS = []
scores = {}

with open('./Data/questions.json', 'r', encoding='utf8') as myFile:
    questions = json.load(myFile)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    for i in range(len(questions)):

        data = f'question{i + 1} is: {questions[i]["question"]}\noptions are: {questions[i]["options"]}'
        ans = ''
        conn.sendall(str.encode(data))

        conn.settimeout(15)

        try:
            ans = conn.recv(1024).decode('utf-8')

        except socket.timeout:
            print('time is over!')

        if ans != '':
            user_name = str(ans).split(':')[0]
            user_answer = str(ans).split(':')[1]

            if int(user_answer) == questions[i]["answer"]:
                if user_name not in scores:
                    scores[user_name] = 0
                scores[user_name] += 1

        print(scores)
        conn.sendall(str.encode(str(scores)))
        time.sleep(5)

    conn.close()


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
    print(f'[ACTIVE CONNECTIONS] {clientCount}')
    CLIENTS.append((conn, addr))
    if len(CLIENTS) == 3:
        for c in CLIENTS:
            threading.Thread(target=handle_client, args=c).start()
