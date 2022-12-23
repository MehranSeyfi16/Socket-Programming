import json
import socket
import threading
import time
from tkinter import *

with open('./Data/questions.json', 'r', encoding='utf8') as myFile:
    questions = json.load(myFile)
scores = {}


class Server:
    def __init__(self):

        self.clientCount = 0
        self.CLIENTS = []
        self.ip = "127.0.0.1"
        self.port = 8080
        self.users = {}

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
            self.clientCount += 1

            name = conn.recv(1024).decode('utf-8')
            if name not in scores:
                scores[name] = 0

            if name not in self.users:
                self.users[name] = (conn, addr)
                print(f"test:{self.users}")

            print(f'[ACTIVE CONNECTIONS] {self.clientCount}')
            self.CLIENTS.append((conn, addr))
            if len(self.CLIENTS) == 3:
                for c in self.CLIENTS:
                    threading.Thread(target=self.handle_client, args=c).start()

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        for i in range(len(questions)):

            data = f'question{i + 1} is: {questions[i]["question"]}\noptions are: {questions[i]["options"]}'
            ans = ''
            conn.sendall(str.encode(data))

            conn.settimeout(5)

            try:
                ans = conn.recv(1024).decode('utf-8')

            except socket.timeout:
                print('time is over!')

            if ans != '':
                user_name = str(ans).split(':')[0]
                user_answer = str(ans).split(':')[1]

                if int(user_answer) == questions[i]["answer"]:
                    scores[user_name] += 1

            # self.scoreboard()
            print(scores)
            time.sleep(5)

        conn.close()

    def scoreboard(self):

        Window = Tk()
        Window.withdraw()

        scoreBoard = Toplevel()
        scoreBoard.title("scoreboard")
        scoreBoard.resizable(width=True,
                             height=True)
        scoreBoard.configure(width=400,
                             height=500)

        pls = Label(scoreBoard,
                    text="ScoreBoard",
                    justify=CENTER,
                    font="Helvetica 20 bold")

        pls.place(relheight=0.15,
                  relx=0.30,
                  rely=0.07)

        playerA = Label(scoreBoard,
                        text=f'{list(scores.keys())[0]}:',
                        font="Helvetica 12")

        playerA.place(relheight=0.15,
                      relx=0.1,
                      rely=0.2)

        scoreA = Label(scoreBoard,
                       font="Helvetica 14",
                       text=list(scores.values())[0])

        scoreA.place(relwidth=0.4,
                     relheight=0.12,
                     relx=0.5,
                     rely=0.2)

        scoreA.focus()

        playerB = Label(scoreBoard,
                        text=f'{list(scores.keys())[1]}:',
                        font="Helvetica 12")

        playerB.place(relheight=0.15,
                      relx=0.1,
                      rely=0.3)

        scoreB = Label(scoreBoard,
                       font="Helvetica 14",
                       text=list(scores.values())[1])

        scoreB.place(relwidth=0.4,
                     relheight=0.12,
                     relx=0.5,
                     rely=0.3)

        scoreB.focus()

        playerC = Label(scoreBoard,
                        text=f'{list(scores.keys())[2]}:',
                        font="Helvetica 12")

        playerC.place(relheight=0.15,
                      relx=0.1,
                      rely=0.4)
        scoreC = Label(scoreBoard,
                       font="Helvetica 14",
                       text=list(scores.values())[1])

        scoreC.place(relwidth=0.4,
                     relheight=0.12,
                     relx=0.5,
                     rely=0.4)

        scoreC.focus()

        # Window.after(3000, lambda: Window.quit())
        Window.mainloop()


s = Server()
s.start_server()
