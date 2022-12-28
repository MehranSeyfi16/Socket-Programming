import socket
import threading
from tkinter import *
import json
import time
from tkinter import messagebox
with open('./Data/users.json', 'r', encoding="utf8") as myFile:
    users = json.load(myFile)

if len(users) != 1:
    del users[0]

with open('./Data/users.json', 'w') as myFile:
    json.dump(users, myFile)


host = "127.0.0.1"
port = users[0]["port"]
print(port)
ADDRESS = (host, port)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def score_counter(i):
    str = f"sry{i}"
    i = i + 1
    return str


with open('./Data/questions.json', 'r', encoding="utf8") as myFile:
    questions = json.load(myFile)

try:
    client_socket.connect((host, port))
except socket.error as e:
    print(str(e))

print(f"[CONNECTED] Client connected to server at {host}:{port}")


class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=True,
                             height=True)
        self.login.configure(width=800,
                             height=400)

        self.pls = Label(self.login,
                         text="Welcome To The Competition! Enter Your Username Please",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)

        self.labelName = Label(self.login,
                               text="Your Username: ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.15,
                             relx=0.2,
                             rely=0.2)

        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)

        self.entryName.focus()

        self.go = Button(self.login,
                         text="Start Game",
                         font="Helvetica 14 bold",
                         command=lambda: self.go_ahead(self.entryName.get()))

        self.go.place(relx=0.4,
                      rely=0.4)

        self.Window.mainloop()

    def go_ahead(self, name):
        self.login.destroy()

        self.layout(name)

        threading.Thread(target=self.receive).start()

    def layout(self, name):
        client_socket.sendall(str.encode(name))
        self.name = name
        self.Window.deiconify()
        self.Window.title("Competition")
        self.Window.resizable(width=False,
                              height=False)

        self.Window.configure(width=900,
                              height=550,
                              bg="#092594")

        self.labelHead = Label(self.Window,
                               bg="#0bbfb0",
                               fg="#000000",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#000000")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#d3e8c5",
                             fg="#000000",
                             font="Helvetica 10",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=0.4,
                            rely=0.08)

        self.chatBox = Text(self.Window,
                            width=20,
                            height=2,
                            bg="#d3e8c5",
                            fg="#000000",
                            font="Helvetica 10",
                            padx=5,
                            pady=5)

        self.chatBox.place(relheight=0.745,
                           relwidth=0.4,
                           rely=0.08,
                           relx=0.403)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#ced6c3",
                              fg="#000000",
                              font="Helvetica 13")

        self.entryMsg.place(relwidth=0.25,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryChat = Entry(self.labelBottom,
                               bg="#ced6c3",
                               fg="#000000",
                               font="Helvetica 13")

        self.entryChat.place(relwidth=0.25,
                             relheight=0.06,
                             rely=0.008,
                             relx=0.4)

        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=10,
                                bg="#ced6c3",
                                command=lambda: self.send_button(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.27,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.12)

        self.chatButton = Button(self.labelBottom,
                                 text="SendChat",
                                 font="Helvetica 10 bold",
                                 width=10,
                                 bg="#ced6c3",
                                 command=lambda: self.chat_button(self.entryChat.get()))

        self.chatButton.place(relx=0.67,
                              rely=0.008,
                              relheight=0.06,
                              relwidth=0.12)

        self.textCons.config(cursor="heart")

        scrollbar = Scrollbar(self.textCons)

        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.listBox = Listbox(self.Window)

        self.listBox.place(relwidth=0.18,
                           relheight=0.345,
                           relx=0.81,
                           rely=0.08)

        self.userNameBox = Listbox(self.Window,relief=RAISED)

        self.userNameBox.place(x=730, y=245, relwidth=0.18, relheight=0.36)

        # self.listBox.pack()

        self.textCons.config(state=DISABLED)

        # second = StringVar()
        # second.set("5")
        #
        # self.secondEntry = Message(textvariable=second, relief=RAISED)
        # self.secondEntry.place(x=180, y=20)
        #
        # def submit():
        #     try:
        #         temp = int(second.get())
        #     except:
        #         print("Please input the right value")
        #     while temp > -1:
        #         mins, secs = divmod(temp, 60)
        #         second.set("{0:2d}".format(secs))
        #         self.secondEntry.update()
        #         time.sleep(1)
        #         if (temp == 0):
        #             messagebox.showinfo("Time Countdown", "Time's up ")
        #         temp -= 1
        #
        # self.btn = Message(bd='5', command=submit())

    def send_button(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.send_message)
        snd.start()

    def chat_button(self, chat):

        self.chat = chat
        self.entryChat.delete(0, END)
        snd = threading.Thread(target=self.send_chat)
        snd.start()

    def receive(self):
        while True:
            message = client_socket.recv(1024).decode('utf-8')

            if message.split("--")[-1].startswith("usernames:"):
                user_names = message.split("--")[1]
                # user_names.replace("usernames:", "")
                message = message.split("--")[0]
                self.userNameBox.insert(0,user_names)

            def submit(second):
                try:
                    temp = int(second.get())
                except:
                    print("Please input the right value")
                while temp > -1:
                    mins, secs = divmod(temp, 60)
                    second.set("{0:2d}".format(secs))
                    self.secondEntry.update()
                    time.sleep(1)
                    # if (temp == 0):
                    #     messagebox.showinfo("Time Countdown", "Time's up ")
                    temp -= 1

            if message.find('{') != -1:
                self.listBox.insert(1, message)
                second = StringVar()
                second.set("5")
                self.secondEntry = Message(textvariable=second, relief=RAISED)
                self.secondEntry.place(x=770, y=475, relwidth=0.1, relheight=0.1, )
                self.btn = Message(bd='5', command=submit(second))


            elif message.find('question') != -1:
                self.listBox.delete(0, END)
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, f"{message}\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
                second1 = StringVar()
                second1.set("10")
                self.secondEntry = Message(textvariable=second1, relief=RAISED)
                self.secondEntry.place(x=770, y=475, relwidth=0.1, relheight=0.1, )
                self.btn = Message(bd='5', command=submit(second1))


            else:
                self.chatBox.config(state=NORMAL)
                self.chatBox.insert(END, f"{message}\n\n")
                self.chatBox.config(state=DISABLED)
                self.chatBox.see(END)
                second2 = StringVar()
                second2.set("15")
                self.secondEntry = Message(textvariable=second2, relief=RAISED)
                self.secondEntry.place(x=770, y=475, relwidth=0.1, relheight=0.1, )
                self.btn = Message(bd='5', command=submit(second2))



    def send_message(self):
        self.textCons.config(state=DISABLED)
        message = f"{self.name}:{self.msg}"
        client_socket.sendall(str.encode(message))

    def send_chat(self):
        self.textCons.config(state=DISABLED)
        message = self.chat
        client_socket.sendall(str.encode(message))
        # self.listBox.delete(0, END)


gui = GUI()
