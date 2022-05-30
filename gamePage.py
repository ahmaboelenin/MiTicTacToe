from tkinter import Canvas, Label, Button, messagebox
from random import sample, choice, shuffle

from assets import sleep, Image, ImageTk, resource_path, ThreadedTask


class GamePage(Canvas):
    def __init__(self, master):
        super().__init__(master=master, bg="#F1F5F5", highlightthickness=0)
        self.gameMode, self.difficultyLevel, self.delay = self.master.gameMode, self.master.difficulty, 100
        self.currentPlayer, self.round = None, 0
        self.oneName, self.twoName = self.master.oneName, self.master.twoName
        self.oneSymbol, self.twoSymbol = self.master.oneSymbol, self.master.twoSymbol
        self.oneScore, self.twoScore, self.drawScore = 0, 0, 0
        self.oneSelects, self.twoSelects = [], []

        self.game_buttons = [
            self.Button(self, text=' ', command=lambda id_=1: self.click(id_), x=11, y=11),
            self.Button(self, text=' ', command=lambda id_=2: self.click(id_), x=105, y=11),
            self.Button(self, text=' ', command=lambda id_=3: self.click(id_), x=199, y=11),
            self.Button(self, text=' ', command=lambda id_=4: self.click(id_), x=11, y=105),
            self.Button(self, text=' ', command=lambda id_=5: self.click(id_), x=105, y=105),
            self.Button(self, text=' ', command=lambda id_=6: self.click(id_), x=199, y=105),
            self.Button(self, text=' ', command=lambda id_=7: self.click(id_), x=11, y=199),
            self.Button(self, text=' ', command=lambda id_=8: self.click(id_), x=105, y=199),
            self.Button(self, text=' ', command=lambda id_=9: self.click(id_), x=199, y=199)]

        self.create_text(218, 289, text="Round", font=("Lato", 12 * -1), fill="#2D3748", anchor="nw")
        self.create_text(260, 289, text=1, tag="round", font=("Lato", 12 * -1), fill="#2D3748", anchor="nw")

        self.turn_label = Label(self, text="Player Turn", width=184, font=("Lato", 20 * -1), bg="#F1F5F5",
                                highlightthickness=0, anchor="n")
        self.turn_label.place(x=11, y=300, width=184)

        self.create_text(11, 334, text='PlayerOne', tag="name", width=125, font=("Lato", 15 * -1, 'bold'),
                         fill="#2D3748", anchor="nw")
        self.create_text(11, 357, text="PlayerTwo", tag="name2", width=125, font=("Lato", 15 * -1, 'bold'),
                         fill="#CD2929", anchor="nw")
        self.create_text(11, 380, text="Draw", width=125, font=("Lato", 15 * -1, 'bold'), fill="#2D3748", anchor="nw")

        self.create_text(150, 335, text="X", tag="symbol", font=("Lato", 13 * -1, 'bold'), fill="#2D3748", anchor="nw")
        self.create_text(150, 358, text="O", tag="symbol2", width=22, font=("Lato", 13 * -1, 'bold'), fill="#CD2929",
                         anchor="nw")

        self.create_text(180, 335, text=self.oneScore, tag="score1", font=("Lato", 13 * -1, 'bold'),
                         fill="#2D3748", anchor="nw")
        self.create_text(180, 358, text=self.twoScore, tag="score2", font=("Lato", 13 * -1, 'bold'),
                         fill="#CD2929", anchor="nw")
        self.create_text(180, 381, text=self.drawScore, tag="score3", font=("Lato", 13 * -1, 'bold'),
                         fill="#2D3748", anchor="nw")

        self.start()
        sleep(0.2)
        self.master.loadingPage.pack_forget()
        self.master.loadingPage.interrupt = True
        self.master.menuBar.show_option_menu(self)
        self.pack(expand=1, fill='both')

    def start(self):
        self.currentPlayer, self.round = "PlayerOne", 1
        self.turn_label.config(text=self.oneName + " Turn")

        self.itemconfigure('name', text=self.oneName)
        self.itemconfigure('name2', text=self.twoName)
        self.itemconfigure('symbol', text=self.oneSymbol)
        self.itemconfigure('symbol2', text=self.twoSymbol)

        if self.difficultyLevel == 'Easy':
            self.difficultyLevel, self.delay = self.easy_play, 150
        else:
            self.difficultyLevel, self.delay = self.hard_play, 100

    def change_player(self):
        if self.currentPlayer == "PlayerOne":
            self.currentPlayer = "PlayerTwo"
            self.turn_label.config(text=self.twoName + " Turn", fg='#CD2929')
            if self.gameMode == 'Single':
                self.after(self.delay, self.difficultyLevel)

        else:
            self.currentPlayer = "PlayerOne"
            self.turn_label.config(text=self.oneName + " Turn", fg="#000000")

    def easy_play(self):
        if 5 not in self.oneSelects + self.twoSelects:
            position = 5
        else:
            position = choice([i for i in range(1, 10) if i not in self.oneSelects + self.twoSelects])
        self.click(position)

    def hard_play(self):
        def analyse():
            solutions = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
            shuffle(solutions)
            if 5 not in lst + lst2:
                return 5

            for solu in solutions:
                if len(set(lst) & set(solu)) == 2:
                    position_ = list(set(solu) - set(lst))[0]
                    if position_ not in lst + lst2:
                        return position_

            for solu in solutions:
                if len(set(lst2) & set(solu)) == 2:
                    position_ = list(set(solu) - set(lst2))[0]
                    if position_ not in lst + lst2:
                        return position_

            return 0

        def minimax():
            position_, value_ = 0, -2

            numbers_ = sample(range(1, 10), (10 - 1))
            for j in numbers_:
                if j not in lst + lst2:
                    lst.append(j)
                    score_ = -minimax()
                    if score_ > value_:
                        value_ = score_
                        position_ = j
                    lst.remove(j)

            if position_ == 0:
                return 0
            return value

        lst2, lst = self.oneSelects, self.twoSelects
        position, value = analyse(), -2
        if position != 0:
            self.click(position)
            return

        numbers = sample(range(1, 10), (10 - 1))
        for i in numbers:
            if i not in lst + lst2:
                lst.append(i)
                score = -minimax()
                if score > value:
                    value = score
                    position = i
                lst.remove(i)
        self.click(position)

    def click(self, id_):
        if self.currentPlayer == "PlayerOne":
            self.game_buttons[id_ - 1].click(self.oneSymbol)
            self.oneSelects.append(id_)
        else:
            self.game_buttons[id_ - 1].click(self.twoSymbol, '#CD2929')
            self.twoSelects.append(id_)

        if self.check():
            self.change_player()

    def check(self):
        solutions = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
        for solu in solutions:
            if set(solu).issubset(set(self.oneSelects)) or set(solu).issubset(set(self.twoSelects)):
                self.end_game(state="win")

        if len(self.oneSelects) + len(self.twoSelects) == 9:
            self.end_game(state="draw")
        return 1

    def end_game(self, state):
        if state == "win":
            if self.currentPlayer == "PlayerOne":
                self.oneScore += 1
                self.itemconfigure('score1', text=self.oneScore)
                messagebox.showinfo("Info", self.oneName + " Wins :)")
            else:
                self.twoScore += 1
                self.itemconfigure('score2', text=self.twoScore)
                messagebox.showinfo("Info", self.twoName + " Wins :)")
        else:
            self.drawScore += 1
            self.itemconfigure('score3', text=self.drawScore)
            messagebox.showinfo("Info", "Draw :)")

        self.start_new_round()

    def start_new_round(self):
        self.oneSelects, self.twoSelects = [], []
        self.round += 1
        self.itemconfigure('round', text=self.round)

        if self.round % 2 == 0:
            self.currentPlayer = "PlayerOne"
            self.turn_label.config(text=self.oneName + " Turn", fg="#000000")
        else:
            self.currentPlayer = "PlayerTwo"
            self.turn_label.config(text=self.twoName + " Turn", fg="#CD2929")
        self.reset_buttons()

    def reset_game(self):
        self.currentPlayer = "PlayerOne"
        self.round, self.oneScore, self.twoScore, self.drawScore = 1, 0, 0, 0
        self.oneSelects, self.twoSelects = [], []

        self.turn_label.configure(text=self.oneName + " Turn", fg="#000000")
        self.itemconfigure('round', text=self.round)
        self.itemconfigure('score1', text=self.oneScore)
        self.itemconfigure('score2', text=self.twoScore)
        self.itemconfigure('score3', text=self.drawScore)
        self.reset_buttons()

    def reset_buttons(self):
        for button in self.game_buttons:
            button.reset(lambda id_=self.game_buttons.index(button) + 1: self.click(id_))

    def return_(self):
        from startPage import StartPage
        self.destroy()
        ThreadedTask(StartPage, self.master)
        self.destroy()
        self.master.menuBar.hide_option_menu()
        self.master.loadingPage.next_frame()
        self.master.loadingPage.pack(expand=1, fill="both")

    class Button:
        def __init__(self, parent, text, command, x, y):
            img = ImageTk.PhotoImage(Image.open(resource_path(r"assets/button_board.png")))
            self.button = Button(parent, text=text, font=("Lato", 48 * -1), image=img, command=command,
                                 compound='center', borderwidth=0, highlightthickness=0, relief="flat",
                                 activebackground="#0096C7", )
            self.button.image = img
            self.button.place(x=x, y=y, width=90, height=90)

        def config(self, state):
            self.button.config(state=state)

        def click(self, text, color="#000000"):
            self.button.config(text=text, command='', fg=color)

        def reset(self, command):
            self.button.config(text=" ", command=command)

        def config(self, *args):
            self.button.config(args)
