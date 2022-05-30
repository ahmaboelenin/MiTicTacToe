from tkinter import Tk, PhotoImage

from assets import ThreadedTask, resource_path

from menuBar import MenuBar
from loadingPage import LoadingPage
from startPage import StartPage


class App(Tk):
    def __init__(self):
        super().__init__()
        self.oneName, self.twoName = None, 'Mi'
        self.oneSymbol, self.twoSymbol = None, None
        self.gameMode, self.difficulty = 'Single', 'Easy'

        self.title("Mi TicTacToe")
        self.iconphoto(False, PhotoImage(file=resource_path(r"assets/icon.png")))
        self.geometry('300x420')
        self.resizable(False, False)

        self.menuBar = MenuBar(self)
        self.loadingPage = LoadingPage(self)
        ThreadedTask(StartPage, self)

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    App().start()
