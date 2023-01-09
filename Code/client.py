import re
import socket
import sys
import threading
from tkinter import *
import json
import time

with open('../Data/users.json', 'r', encoding="utf8") as myFile:
    users = json.load(myFile)






class Client:

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    names = []

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = users[int(sys.argv[1])]["port"]

        for user in users:
            Client.names.append(user['name'])

    def start_client(self):

        Client.client_socket.bind((self.ip, self.port))

        try:
            Client.client_socket.connect((self.ip, users[0]["port"]))
        except socket.error as e:
            print(str(e))

        print(f"[CONNECTED] Client connected to server at {self.ip}:{self.port}")


class GUI:
    def __init__(self):

        self.timerEntry = None
        self.answerFlag = False
        self.chatFlag = False
        self.chat = None
        self.answer = None
        self.userNameBox = None
        self.scoreBox = None
        self.chatButton = None
        self.answerButton = None
        self.entryChat = None
        self.entryAnswer = None
        self.labelBottom = None
        self.chatBox = None
        self.questionBox = None
        self.line = None
        self.labelHead = None
        self.name = Client.names[int(sys.argv[1])]
        self.root = None

    def root_window(self):
        Client.client_socket.sendall(str.encode(self.name))
        self.root = Tk()
        self.root.withdraw()
        self.root.deiconify()
        self.root.title("Competition")
        self.root.resizable(width=False,
                            height=False)

        self.root.configure(width=900,
                            height=550,
                            bg="#991532")

        self.labelHead = Label(self.root,
                               bg="#991532",
                               fg="#FEC84D",
                               text=self.name,
                               font=("showcard gothic", 16, "bold"),
                               pady=5)

        self.labelHead.place(relwidth=1)

        self.line = Label(self.root,
                          width=450,
                          bg="#991532")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.questionBox = Text(self.root,
                                width=20,
                                height=2,
                                bg="#F2F1E8",
                                fg="#000000",
                                font=("Farsi Kamran Bold", 15, "bold"),
                                padx=5,
                                pady=5)

        self.questionBox.place(relheight=0.745,
                               relwidth=0.4,
                               rely=0.08)

        self.questionBox.config(cursor="heart")
        self.questionBox.config(state=DISABLED)

        self.chatBox = Text(self.root,
                            width=20,
                            height=2,
                            bg="#F2F1E8",
                            fg="#000000",
                            font=("Comic Sans MS", 15),
                            padx=5,
                            pady=5)

        self.chatBox.place(relheight=0.745,
                           relwidth=0.4,
                           rely=0.08,
                           relx=0.403)
        self.chatBox.config(cursor="heart")
        self.chatBox.config(state=DISABLED)

        self.labelBottom = Label(self.root,
                                 bg="#991532",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryAnswer = Entry(self.labelBottom,
                                 bg="#F2F1E8",
                                 fg="#000000",
                                 font=("Comic Sans MS", 20))

        self.entryAnswer.place(relwidth=0.25,
                               relheight=0.06,
                               rely=0.008,
                               relx=0.011)

        self.entryAnswer.focus()

        self.entryChat = Entry(self.labelBottom,
                               bg="#F2F1E8",
                               fg="#000000",
                               font=("Comic Sans MS", 15))

        self.entryChat.place(relwidth=0.25,
                             relheight=0.06,
                             rely=0.008,
                             relx=0.42)

        self.answerButton = Button(self.labelBottom,
                                   text="Send",
                                   font=("showcard gothic", 16, "bold"),
                                   width=10,
                                   bg="#FEC84D",
                                   fg="#004369",
                                   command=lambda: self.send_button(self.entryAnswer.get()))

        self.answerButton.place(relx=0.27,
                                rely=0.008,
                                relheight=0.06,
                                relwidth=0.12)

        self.chatButton = Button(self.labelBottom,
                                 text="Chat",
                                 font=("showcard gothic", 16, "bold"),
                                 width=10,
                                 bg="#FEC84D",
                                 fg="#004369",
                                 command=lambda: self.chat_button(self.entryChat.get()))

        self.chatButton.place(relx=0.68,
                              rely=0.008,
                              relheight=0.06,
                              relwidth=0.12)

        scrollbar = Scrollbar(self.questionBox)

        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.questionBox.yview)

        self.scoreBox = Listbox(self.root, background='#F2F1E8', font=("Comic Sans MS", 12))

        self.scoreBox.place(relwidth=0.18,
                            relheight=0.345,
                            relx=0.81,
                            rely=0.08)

        self.userNameBox = Listbox(self.root, relief=RAISED, background='#F2F1E8', font=("Comic Sans MS", 12))
        self.userNameBox.place(x=730, y=245, relwidth=0.18, relheight=0.38)
        self.userNameBox.insert(END, "users:\n")
        for i in range(1, len(Client.names)):
            self.userNameBox.insert(END, Client.names[i])

        threading.Thread(target=self.receive).start()
        self.root.mainloop()

    def send_button(self, answer):
        self.answer = answer
        self.entryAnswer.delete(0, END)
        threading.Thread(target=self.send_message).start()

    def chat_button(self, chat):
        self.chat = chat
        self.entryChat.delete(0, END)
        threading.Thread(target=self.send_chat).start()

    def submit(self, second):

        timer_value = int(second.get())

        try:
            temp = int(second.get())
        except:
            print("Please input the right value")
        while True:
            minutes, secs = divmod(temp, 60)
            second.set("{0:2d}".format(secs))
            self.timerEntry.update()
            time.sleep(1)

            if temp == 0 and timer_value == 45:
                self.userNameBox.insert(END, "Time is up!")
                break

            elif temp == 0 and timer_value == 5:
                self.userNameBox.delete(END)
                self.userNameBox.insert(END, "Now you can chat.")
                self.chatFlag = True
                temp = 21
                timer_value = 21

            elif temp == 0 and timer_value == 21:
                self.userNameBox.delete(END)
                self.userNameBox.insert(END, "Time for chat is up!")
                self.chatFlag = False
                temp = 6
                timer_value = 0

            elif temp == 0 and timer_value == 0:
                self.userNameBox.delete(END)

                break

            temp -= 1

    def receive(self):
        while True:
            message = Client.client_socket.recv(1024).decode('utf-8')

            # question
            if message.find('question') != -1:
                self.questionBox.config(state=NORMAL)
                self.questionBox.delete("1.0", END)
                question = message.split('\n')[0].lstrip('question')
                question = re.sub(r'[0-9]', '', question)
                question = question.lstrip(':')
                options = (message.split('\n')[1]).split(',')
                option1 = options[0].lstrip('[').replace("'", '')
                option2 = options[1].replace("'", '')
                option3 = options[2].replace("'", '')
                option4 = options[3].rstrip(']').replace("'", '')

                self.answerFlag = True
                self.scoreBox.delete(0, END)

                self.questionBox.insert(END, f"{question}\n")
                self.questionBox.insert(END, f"1) {option1}\n")
                self.questionBox.insert(END, f"2){option2}\n")
                self.questionBox.insert(END, f"3){option3}\n")
                self.questionBox.insert(END, f"4){option4}\n")
                self.questionBox.config(state=DISABLED)
                self.questionBox.see(END)
                second1 = StringVar()
                second1.set("45")
                self.timerEntry = Message(textvariable=second1, relief=RAISED, background='#004369', foreground="white",
                                          font=("showcard gothic", 16, "bold"))
                self.timerEntry.place(x=770, y=475, relwidth=0.1, relheight=0.1)
                threading.Thread(target=self.submit, args=(second1,)).start()

            # scoreboard
            elif message.find('scores') != -1:
                self.answerFlag = False
                scores = message.split('@')[1].lstrip('{').rstrip('}').split(',')
                for score in scores:
                    self.scoreBox.insert(END, score.replace("'", ''))

                second = StringVar()
                second.set("5")
                self.timerEntry = Message(textvariable=second, relief=RAISED, background='#004369', foreground="white",
                                          font=("showcard gothic", 16, "bold"))
                self.timerEntry.place(x=770, y=475, relwidth=0.1, relheight=0.1)
                threading.Thread(target=self.submit, args=(second,)).start()

            elif message.find('finish') != -1:
                break

            # chat
            else:
                self.chatBox.config(state=NORMAL)
                self.chatBox.insert(END, f"{message}\n")
                self.chatBox.config(state=DISABLED)
                self.chatBox.see(END)

        Client.client_socket.close()
        self.root.destroy()

    def send_message(self):
        message = f"{self.name}:{self.answer}"
        if self.answerFlag:
            Client.client_socket.sendall(str.encode(message))
            self.answerFlag = False

    def send_chat(self):
        if self.chatFlag:
            Client.client_socket.sendall(str.encode(self.chat))


c = Client()
c.start_client()
gui = GUI()
gui.root_window()
