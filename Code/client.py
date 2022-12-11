import socket
import threading
from tkinter import *
import json

host = "127.0.0.1"
port = 8080
ADDRESS = (host, port)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with open('Data\questions.json', 'r', encoding="utf8") as myFile:
    questions = json.load(myFile)

try:
    client_socket.connect((host, port))
except socket.error as e:
    print(str(e))

print(f"[CONNECTED] Client connected to server at {host}:{port}")


# connected = True
# while connected:
#     data = client_socket.recv(1024)
#     print(data.decode('utf-8'))
#     answer = input('write your answer: ')
#     client_socket.send(str.encode(answer))

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

        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def layout(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("Competition")
        self.Window.resizable(width=False,
                              height=False)

        self.Window.configure(width=470,
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
                             relheight=0.06,
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

    def receive(self):
        while True:
            try:
                message = client_socket.recv(1024)
                print(message.decode('utf-8'))

                if message == 'NAME':
                    client_socket.send(self.name.encode("utf-8"))
                else:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         message + "\n\n".encode())

                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                print("An error occurred!")
                client_socket.close()
                break

    def send_message(self):
        self.textCons.config(state=DISABLED)

        while True:
            message = (f"{self.name}: {self.msg}")
            client_socket.send(message.encode("utf-8"))
            break
    # def check_score(self):
    #
    #     if int(self.msg) == str(questions[qcount]["answer"]):
    #         scores.update(self.name)
    #         scores[self.name] += 1
    #         print(scores)


gui = GUI()
