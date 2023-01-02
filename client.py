import socket
import sys
import threading
from tkinter import *
import json
import time

with open('./Data/users.json', 'r', encoding="utf8") as myFile:
    users = json.load(myFile)

names = []

for user in users:
    names.append(user['name'])

host = "127.0.0.1"
port = users[int(sys.argv[1])]["port"]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind((host, port))

try:
    client_socket.connect((host, users[0]["port"]))
except socket.error as e:
    print(str(e))

print(f"[CONNECTED] Client connected to server at {host}:{port}")


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
        self.name = names[int(sys.argv[1])]
        self.root = None

    def root_window(self):
        client_socket.sendall(str.encode(self.name))
        self.root = Tk()
        self.root.withdraw()
        self.root.deiconify()
        self.root.title("Competition")
        self.root.resizable(width=False,
                            height=False)

        self.root.configure(width=900,
                            height=550,
                            bg="#AD5858")

        self.labelHead = Label(self.root,
                               bg="#AD5858",
                               fg="#000000",
                               text=self.name,
                               font="Ebrima 20 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)

        self.line = Label(self.root,
                          width=450,
                          bg="#AD5858")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.questionBox = Text(self.root,
                                width=20,
                                height=2,
                                bg="#C4D1DE",
                                fg="#000000",
                                font="Helvetica 12",
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
                            bg="#C4D1DE",
                            fg="#000000",
                            font="Helvetica 15",
                            padx=5,
                            pady=5)

        self.chatBox.place(relheight=0.745,
                           relwidth=0.4,
                           rely=0.08,
                           relx=0.403)
        self.chatBox.config(cursor="heart")
        self.chatBox.config(state=DISABLED)

        self.labelBottom = Label(self.root,
                                 bg="#AD5858",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryAnswer = Entry(self.labelBottom,
                                 bg="#C4D1DE",
                                 fg="#000000",
                                 font="Helvetica 13")

        self.entryAnswer.place(relwidth=0.25,
                               relheight=0.06,
                               rely=0.008,
                               relx=0.011)

        self.entryAnswer.focus()

        self.entryChat = Entry(self.labelBottom,
                               bg="#C4D1DE",
                               fg="#000000",
                               font="Helvetica 13")

        self.entryChat.place(relwidth=0.25,
                             relheight=0.06,
                             rely=0.008,
                             relx=0.42)

        self.answerButton = Button(self.labelBottom,
                                   text="Send",
                                   font="Helvetica 10 bold",
                                   width=10,
                                   bg="#C4D1DE",
                                   command=lambda: self.send_button(self.entryAnswer.get()))

        self.answerButton.place(relx=0.27,
                                rely=0.008,
                                relheight=0.06,
                                relwidth=0.12)

        self.chatButton = Button(self.labelBottom,
                                 text="SendChat",
                                 font="Helvetica 10 bold",
                                 width=10,
                                 bg="#C4D1DE",
                                 command=lambda: self.chat_button(self.entryChat.get()))

        self.chatButton.place(relx=0.68,
                              rely=0.008,
                              relheight=0.06,
                              relwidth=0.12)

        scrollbar = Scrollbar(self.questionBox)

        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.questionBox.yview)

        self.scoreBox = Listbox(self.root, background='#C4D1DE', font='Helvetica 10 bold')

        self.scoreBox.place(relwidth=0.18,
                            relheight=0.345,
                            relx=0.81,
                            rely=0.08)

        self.userNameBox = Listbox(self.root, relief=RAISED, background='#C4D1DE')
        self.userNameBox.place(x=730, y=245, relwidth=0.18, relheight=0.38)
        self.userNameBox.insert(0, str(names[1:]))

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

            if temp == 0 and timer_value == 30:
                self.userNameBox.delete(1, END)
                self.userNameBox.insert(1, "Time is up!")
                break

            elif temp == 0 and timer_value == 5:
                self.userNameBox.delete(1, END)
                self.userNameBox.insert(1, "Now you can chat with others.")
                self.chatFlag = True
                temp = 21
                timer_value = 21

            elif temp == 0 and timer_value == 21:
                self.userNameBox.delete(1, END)
                self.userNameBox.insert(1, "Time for chat is up!")
                self.chatFlag = False
                temp = 6
                timer_value = 0

            elif temp == 0 and timer_value == 0:
                self.userNameBox.delete(1, END)
                self.userNameBox.insert(1, 'next question...')
                break

            temp -= 1

    def receive(self):
        while True:
            message = client_socket.recv(1024).decode('utf-8')

            # question
            if message.find('question') != -1:
                self.answerFlag = True
                self.scoreBox.delete(0, END)
                self.questionBox.config(state=NORMAL)
                self.questionBox.insert(END, f"{message}\n\n")
                self.questionBox.config(state=DISABLED)
                self.questionBox.see(END)
                second1 = StringVar()
                second1.set("30")
                self.timerEntry = Message(textvariable=second1, relief=RAISED, background='#C4D1DE',
                                          font='Helvetica 15 bold')
                self.timerEntry.place(x=770, y=475, relwidth=0.1, relheight=0.1)
                threading.Thread(target=self.submit, args=(second1,)).start()

            # scoreboard
            elif message.find('scores') != -1:
                self.answerFlag = False
                scores = message.split('@')[1].lstrip('{').rstrip('}').split(',')
                for score in scores:
                    self.scoreBox.insert(END, score)

                second = StringVar()
                second.set("5")
                self.timerEntry = Message(textvariable=second, relief=RAISED, background='#C4D1DE',
                                          font='Helvetica 15 bold')
                self.timerEntry.place(x=770, y=475, relwidth=0.1, relheight=0.1)
                threading.Thread(target=self.submit, args=(second,)).start()

            elif message.find('finish') != -1:
                break

            # chat
            else:
                self.chatBox.config(state=NORMAL)
                self.chatBox.insert(END, f"{message}\n\n")
                self.chatBox.config(state=DISABLED)
                self.chatBox.see(END)

        client_socket.close()
        self.root.destroy()

    def send_message(self):
        message = f"{self.name}:{self.answer}"
        if self.answerFlag:
            client_socket.sendall(str.encode(message))

    def send_chat(self):
        if self.chatFlag:
            client_socket.sendall(str.encode(self.chat))


gui = GUI()
gui.root_window()