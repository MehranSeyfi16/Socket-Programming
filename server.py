import json
import socket
import threading
import time
from datetime import datetime

host = "127.0.0.1"
port = 8080
clientCount = 0
CLIENTS = []
scores = {}
users = {}

with open('./Data/questions.json', 'r', encoding='utf8') as myFile:
    questions = json.load(myFile)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    for i in range(len(questions)):

        data = f'question{i + 1} is: {questions[i]["question"]}\noptions are: {questions[i]["options"]}'
        ans = ''

        conn.sendall(str.encode(data))
        send_time = datetime.now()
        conn.settimeout(35)

        try:
            ans = conn.recv(1024).decode('utf-8')
            recv_time = datetime.now()
            time.sleep(35 - ((recv_time - send_time).total_seconds()))
            print('time for question is over!')

        except socket.timeout:
            print('time for question is over! empty answer!')

        if ans != '':
            user_name = str(ans).split(':')[0]
            user_answer = str(ans).split(':')[1]

            if int(user_answer) == questions[i]["answer"]:
                scores[user_name] += 1


        conn.sendall(str.encode(str(scores)))
        time.sleep(5)

        print('chat room started...')
        time1 = datetime.now()
        conn.settimeout(25)

        try:
            message = conn.recv(1024).decode('utf-8')
            time2 = datetime.now()

            if message != '':
                chat = message.split('-')[0]
                key_list = list(users.keys())
                val_list = list(users.values())
                position = val_list.index((conn, addr))
                source_user = key_list[position]
                dest_user = message.split('-')[1]
                dest_conn = users[dest_user][0]
                dest_conn.sendall(str.encode(f'{source_user}: {chat}'))

            time.sleep(25 - ((time2 - time1).total_seconds()))
            print('time for chat is over!')

        except socket.timeout:
            print('time is over! empty chat!')

        time.sleep(5)
        print('next question...')

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
    name = conn.recv(1024).decode('utf-8')

    if name not in users:
        users[name] = (conn, addr)

    if name not in scores:
        scores[name] = 0


    clientCount += 1
    print(f'[ACTIVE CONNECTIONS] {clientCount}')
    CLIENTS.append((conn, addr))
    if len(CLIENTS) == 3:
        for c in CLIENTS:
            threading.Thread(target=handle_client, args=c).start()
