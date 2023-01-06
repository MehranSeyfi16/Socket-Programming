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
        os.system(f'python server.py {len(users) - 1}')

    def exit(self):
        sys.exit()

    def guide(self):
        self.guideWindow = Toplevel(self.root, background='#32a1a1')
        self.guideWindow.title("Guide")
        self.guideWindow.geometry("400x160")
        msg = Label(self.guideWindow, background='#41bcbc', text=f'Competition rules:\n First of all, the first question will be sent to you,\n   and you have 45 seconds to answer that,\n     meanwhile, only the first answer you sent will be considered\n     and no points will be given to the subsequent answers.\n    Then the scoreboard will be displayed in 5 seconds,\n    after that, time is included for you to chat, and you can send a message \n     to the desired user with the syntax chat#username. After the chat time ends, \n     the next question is sent and the same process continues.\n')
        msg.pack()


main = GUI()
main.root_window()
