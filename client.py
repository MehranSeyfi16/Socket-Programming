import json
import socket
import threading
import time
from tkinter import *


class Client:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 8080

    def start_client(self):

        try:
            self.client_socket.connect((self.ip, self.port))
        except socket.error as e:
            print(str(e))

        print(f"[CONNECTED] Client connected to server at {self.ip}:{self.port}")


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
        Client.client_socket.sendall(str.encode(name))
        self.name = name
        self.Window.deiconify()
        self.Window.title("Competition")
        self.Window.resizable(width=False,
                              height=False)

        self.Window.configure(width=600,
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

                             bg="#d3e8c5",
                             fg="#000000",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#ced6c3",
                              fg="#000000",
                              font="Helvetica 13")

        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ced6c3",
                                command=lambda: self.send_button(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.03,
                             relwidth=0.22)

        self.buttonChat = Button(self.labelBottom,
                                 text="Chat",
                                 font="Helvetica 10 bold",
                                 width=20,
                                 bg="#ced6c3",
                                 command=lambda: self.chat_room())

        self.buttonChat.place(relx=0.77,
                              rely=0.040,
                              relheight=0.03,
                              relwidth=0.22)

        self.textCons.config(cursor="heart")

        scrollbar = Scrollbar(self.textCons)

        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    def send_button(self, msg):
        self.textCons.config(state=DISABLED)

        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.send_message)
        snd.start()

    def chat_room(self):
        pass
        # self.textCons.config(state=NORMAL)
        # print(server.Server().return_users())
        # # self.textCons.insert(END, f"{list(userss.keys())[0]}\n\n")
        # # self.textCons.insert(END, f"{list(userss.keys())[1]}\n\n")
        # # self.textCons.insert(END, f"{list(userss.keys())[2]}\n\n")
        #
        # self.textCons.config(state=DISABLED)
        # self.textCons.see(END)

    def receive(self):
        while True:
            message = Client.client_socket.recv(1024).decode('utf-8')

            self.textCons.config(state=NORMAL)

            self.textCons.insert(END, f"{message}\n\n")

            self.textCons.config(state=DISABLED)
            self.textCons.see(END)

    def send_message(self):
        self.textCons.config(state=DISABLED)

        message = f"{self.name}:{self.msg}"
        Client.client_socket.sendall(str.encode(message))


c = Client()
c.start_client()
gui = GUI()
