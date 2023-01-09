import json
import socket
import sys
import threading
import time
from datetime import datetime
import multiprocessing

with open('../Data/users.json', 'r', encoding="utf8") as myFile:
    users_file = json.load(myFile)

with open('../Data/questions.json', 'r', encoding='utf8') as myFile:
    questions = json.load(myFile)


class Server:

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = users_file[0]["port"]
        self.clientCount = 0
        self.CLIENTS = []
        self.users = {}
        self.scores = {}

        for i in range(1, len(users_file)):
            name = users_file[i]['name']
            self.scores[name] = 0

    def chatroom(self, connection, address):
        connection.setblocking(True)
        while True:

            message = connection.recv(1024).decode('utf-8')

            if message != '':
                chat = message.split('>')[0]
                key_list = list(self.users.keys())
                val_list = list(self.users.values())
                position = val_list.index((connection, address))
                source_user = key_list[position]
                dest_user = message.split('>')[1]
                dest_conn = self.users[dest_user][0]
                dest_conn.sendall(str.encode(f'{source_user}: {chat}'))

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        for i in range(len(questions)):

            data = f'question{i + 1}: {questions[i]["question"]}\n{questions[i]["options"]}'
            ans = ''
            conn.sendall(str.encode(data))
            send_time = datetime.now()

            conn.settimeout(46.5)

            try:
                ans = conn.recv(1024).decode('utf-8')
                recv_time = datetime.now()
                time.sleep(46.5 - ((recv_time - send_time).total_seconds()))
                print('time for question is over!')

            except socket.timeout:
                print('time for question is over! empty answer!')

            if ans != '':
                user_name = str(ans).split(':')[0]
                user_answer = str(ans).split(':')[1]

                if int(user_answer) == questions[i]["answer"]:
                    self.scores[user_name] += 1

            temp_time = datetime.now().time().microsecond
            time.sleep((1000000 - temp_time) / 1000000)

            conn.sendall(str.encode(f'scores@{str(self.scores)}'))
            time.sleep(6.2)

            print('chat room started...')
            conn.settimeout(None)
            process2 = multiprocessing.Process(target=self.chatroom, args=(conn, addr))
            process2.start()
            process2.join(21.3)
            process2.terminate()

            print('finish chatroom')
            time.sleep(6)

        conn.sendall(str.encode('finish'))

    def start_server(self):
        print('[STARTING] Server is starting...')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((self.ip, self.port))
        except socket.error as e:
            print(str(e))

        server_socket.listen()
        print(f'[LISTENING] Server is listing on {self.ip}:{self.port}')

        while True:
            conn, addr = server_socket.accept()
            name = conn.recv(1024).decode('utf-8')

            if name not in self.users:
                self.users[name] = (conn, addr)

            self.clientCount += 1
            print(f'[ACTIVE CONNECTIONS] {self.clientCount}')
            self.CLIENTS.append((conn, addr))
            if len(self.CLIENTS) == int(sys.argv[1]):
                for c in self.CLIENTS:
                    threading.Thread(target=self.handle_client, args=c).start()


if __name__ == '__main__':
    s = Server()
    s.start_server()
