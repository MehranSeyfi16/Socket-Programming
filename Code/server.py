import json
import socket
import threading
import time

host = "127.0.0.1"
port = 8080
# scores = {"playerA": 0, "playerB": 0, "playerC": 0}
clientCount = 0
CLIENTS = []
scores = {}

with open('Data/questions.json', 'r', encoding='utf8') as myFile:
    questions = json.load(myFile)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    for i in range(len(questions)):

        data = f'question{i + 1} is: {questions[i]["question"]}\noptions are: {questions[i]["options"]}'


        # conn.sendall(str.encode(data))
        broadcast(str.encode(data), conn)
        time.sleep(5)

        # for c in CLIENTS:
        #     c[0].sendall(str.encode(data))

        ans = conn.recv(1024).decode('utf-8')
        print(ans[0:1])
        # print(addr[1])
        # print(conn.getpeername()[1])
        # if ans == str(questions[i]["answer"]):
        #     pass

        # print(int(ans[3:len(ans)]))
        # print(questions[i]["answer"])

        user_answer = ans[3:len(ans)]
        user_name = ans[0:1]

        if int(user_answer) == questions[i]["answer"]:
            if user_name not in scores:
                scores[user_name] = 0
            scores[user_name] += 1

    print(scores)


print('[STARTING] Server is starting...')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind((host, port))
except socket.error as e:
    print(str(e))

server_socket.listen()
print(f'[LISTENING] Server is listing on {host}:{port}')


def broadcast(message, connection):
    for clients in CLIENTS:
        try:
            clients[0].sendall(message)
        except:
            clients[0].close()

            # if the link is broken, we remove the client
            remove(clients)


def remove(connection):
    CLIENTS.remove(connection)


while True:
    conn, addr = server_socket.accept()
    clientCount += 1
    CLIENTS.append((conn, addr))
    if len(CLIENTS) == 3:
        for c in CLIENTS:
            threading.Thread(target=handle_client, args=c).start()
    print(f'[ACTIVE CONNECTIONS] {clientCount}')
