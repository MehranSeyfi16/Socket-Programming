import json
import socket
import sys
import threading
import time
from datetime import datetime
import multiprocessing

with open('./Data/users.json', 'r', encoding="utf8") as myFile:
    users_file = json.load(myFile)

with open('./Data/questions.json', 'r', encoding='utf8') as myFile:
    questions = json.load(myFile)

host = "127.0.0.1"
port = users_file[0]["port"]
clientCount = 0
CLIENTS = []
users = {}
scores = {}

for i in range(1, len(users_file)):
    name = users_file[i]['name']
    scores[name] = 0


def chatroom(connection, address, users):
    connection.setblocking(True)
    while True:

        message = connection.recv(1024).decode('utf-8')

        if message != '':
            chat = message.split('>')[0]
            key_list = list(users.keys())
            val_list = list(users.values())
            position = val_list.index((connection, address))
            source_user = key_list[position]
            dest_user = message.split('>')[1]
            dest_conn = users[dest_user][0]
            dest_conn.sendall(str.encode(f'{source_user}: {chat}'))


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    for i in range(len(questions)):

        data = f'question{i + 1}: {questions[i]["question"]}\n{questions[i]["options"]}'
        ans = ''
        conn.sendall(str.encode(data))
        send_time = datetime.now()

        conn.settimeout(31.5)

        try:
            ans = conn.recv(1024).decode('utf-8')
            recv_time = datetime.now()
            time.sleep(31.5 - ((recv_time - send_time).total_seconds()))
            print('time for question is over!')

        except socket.timeout:
            print('time for question is over! empty answer!')

        if ans != '':
            user_name = str(ans).split(':')[0]
            user_answer = str(ans).split(':')[1]

            if int(user_answer) == questions[i]["answer"]:
                scores[user_name] += 1

        temp_time = datetime.now().time().microsecond
        time.sleep((1000000 - temp_time) / 1000000)

        conn.sendall(str.encode(f'scores@{str(scores)}'))
        time.sleep(6.2)

        print('chat room started...')
        conn.settimeout(None)
        process2 = multiprocessing.Process(target=chatroom, args=(conn, addr, users))
        process2.start()
        process2.join(21.3)
        process2.terminate()

        print('finish chatroom')
        time.sleep(6)

    conn.sendall(str.encode('finish'))


if __name__ == '__main__':
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

        clientCount += 1
        print(f'[ACTIVE CONNECTIONS] {clientCount}')
        CLIENTS.append((conn, addr))
        if len(CLIENTS) == int(sys.argv[1]):
            for c in CLIENTS:
                threading.Thread(target=handle_client, args=c).start()
