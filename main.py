import json
import sys
import os
from tkinter import *

with open('./Data/users.json', 'r', encoding="utf8") as myFile:
    users = json.load(myFile)


class GUI:

    def __init__(self):
        self.root = None
        self.bg = None
        self.label1 = None
        self.startButton = None
        self.guideButton = None
        self.exitButton = None
        self.guideWindow = None

    def root_window(self):
        self.root = Tk()

        self.root.title("QuizOfKings")
        self.root.resizable(width=True,
                            height=True)
        self.root.configure(width=512,
                            height=512)

        self.bg = PhotoImage(file="pic.png")

        self.label1 = Label(self.root, image=self.bg)
        self.label1.place(x=0, y=0)

        self.startButton = Button(self.root, text="New Game", background='#00F321', font='Chiller 30 bold',
                                  command=self.start_game)
        self.startButton.place(x=330,
                               y=400,
                               width=130,
                               height=100)

        self.guideButton = Button(self.root, text="Guide", background='#FFB900', font='Chiller 30 bold',
                                  command=self.guide)
        self.guideButton.place(x=190,
                               y=400,
                               width=130,
                               height=100)

        self.exitButton = Button(self.root, text="Exit", background='#FF0000', font='Chiller 30 bold',
                                 command=self.exit)
        self.exitButton.place(x=50,
                              y=400,
                              width=130,
                              height=100)

        self.root.mainloop()

    def start_game(self):
        self.root.destroy()
        os.system(f'python server.py {len(users) - 1} 8081 8082 8083')

    def exit(self):
        sys.exit()

    def guide(self):
        self.guideWindow = Toplevel(self.root, background='#BCB341')
        self.guideWindow.title("Guide")
        self.guideWindow.geometry("300x300")
        msg = Label(self.guideWindow, background='#BCB341', text=f'rules')
        msg.pack()


main = GUI()
main.root_window()
