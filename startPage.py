from tkinter import Canvas, Entry, Button, messagebox, StringVar, BooleanVar
from tkinter.ttk import Style, Checkbutton, Radiobutton, Separator

from assets import sleep, Image, ImageTk, resource_path, ThreadedTask
from gamePage import GamePage


class StartPage(Canvas):
    def __init__(self, master):
        super().__init__(master=master, bg="#F1F5F5", highlightthickness=0)
        self.duo_play, self.symbol, self.difficulty = BooleanVar(), StringVar(), StringVar()
        self.duo_play.set(0)
        self.symbol.set('X')
        self.difficulty.set('Easy')

        self.style = Style()
        self.style.configure('TCheckbutton', background="#F1F5F5", font=("Roboto", 15 * -1), fill="#2D3748")
        self.style.configure('TRadiobutton', background="#F1F5F5", font=("Roboto", 18 * -1), fill="#2D3748")

        '''____Player_One_Section____'''
        image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/entry.png")))
        self.image = image
        self.create_image(10, 58, image=image, anchor='nw')
        self.create_image(10, 112, image=image, anchor='nw')
        self.create_image(10, 256, image=image, anchor='nw')

        self.create_text(10, 10, text="PlayerOne", font=("Roboto", 32 * -1, 'bold'), fill="#2D3748", anchor="nw")
        self.create_text(18, 58, text="Name", font=("Roboto", 15 * -1), fill="#2D3748", anchor="nw")
        self.oneNameEntry = Entry(self, font=("Roboto", 18 * -1), bd=0, bg="#F1F5F5", highlightthickness=0)
        self.oneNameEntry.place(x=78, y=62, width=202, height=36)

        self.create_text(18, 112, text="Symbol", font=("Roboto", 15 * -1), fill="#2D3748", anchor="nw")

        Radiobutton(self, text='  X', variable=self.symbol, value='X').place(x=78, y=125)
        Radiobutton(self, text='  O', variable=self.symbol, value='O').place(x=179, y=125)

        Radiobutton(self, text=' Easy', variable=self.difficulty, value='Easy').place(x=50, y=166)
        Radiobutton(self, text=' Hard', variable=self.difficulty, value='Hard').place(x=175, y=166)

        Separator(self, orient='horizontal').place(x=0, y=194, width=300, height=4)

        '''____Player_Two_Section____'''
        self.create_text(10, 208, text="PlayerTwo", font=("Roboto", 32 * -1, 'bold'), fill="#CD2929", anchor="nw")

        Checkbutton(self, text="Duo Play", takefocus=0, variable=self.duo_play, command=self.player_two_trigger,
                    onvalue=1, offvalue=0).place(x=210, y=230)

        self.create_text(18, 256, text="Name", font=("Roboto", 15 * -1), fill="#2D3748", anchor="nw")
        self.twoNameEntry = Entry(self, font=("Roboto", 18 * -1), bd=0, bg="#F1F5F5", highlightthickness=0,
                                  state='disabled')
        self.twoNameEntry.place(x=78, y=260, width=202, height=36)

        '''_____Buttons_____'''
        image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/button_start.png")))
        temp = Button(self, image=image, borderwidth=0, highlightthickness=0, relief="flat", command=self.start)
        temp.img = image
        temp.place(x=10, y=310, width=280, height=40)

        image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/button_clear.png")))
        temp = Button(self, image=image, borderwidth=0, highlightthickness=0, relief="flat", command=self.clear)
        temp.img = image
        temp.place(x=10, y=360, width=135, height=40)

        image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/button_exit.png")))
        temp = Button(self, image=image, borderwidth=0, highlightthickness=0, relief="flat", command=self.exit)
        temp.img = image
        temp.place(x=155, y=360, width=135, height=40)

        self.oneNameEntry.bind("<Return>", self.start)
        self.twoNameEntry.bind("<Return>", self.start)

        sleep(0.2)
        self.master.loadingPage.pack_forget()
        self.master.loadingPage.interrupt = True
        self.oneNameEntry.focus_set()
        self.pack(expand=1, fill='both')

    def player_two_trigger(self):
        if self.duo_play.get():
            self.twoNameEntry.config(state='normal')
        else:
            self.twoNameEntry.config(state='disabled')

    def chk_player(self, player):
        if player == 'PlayerOne':
            if self.oneNameEntry.get() != '':
                return 1
            else:
                messagebox.showwarning("Warning", "Please Enter Player's One Name")
        else:
            if self.twoNameEntry.get() != '':
                return 1
            else:
                messagebox.showwarning("Warning", "Please Enter Player's Two Name")

    def start(self, event=None):
        if self.chk_player('PlayerOne'):
            self.master.oneName = self.oneNameEntry.get()
            self.master.oneSymbol = self.symbol.get()
            self.master.difficulty = self.difficulty.get()

            if self.master.oneSymbol == "X":
                self.master.twoSymbol = "O"
            else:
                self.master.twoSymbol = "X"

            if self.duo_play.get():
                if self.chk_player('PlayerTwo'):
                    self.master.gameMode = 'Multi'
                    self.master.twoName = self.twoNameEntry.get()
                else:
                    return

            ThreadedTask(GamePage, self.master)
            self.destroy()
            self.master.loadingPage.next_frame()
            self.master.loadingPage.pack(expand=1, fill="both")

    def clear(self):
        self.duo_play.set(0)
        self.symbol.set('X')
        self.difficulty.set('Easy')
        self.oneNameEntry.delete(0, 'end')
        if self.twoNameEntry["state"] == 'normal':
            self.twoNameEntry.delete(0, 'end')
        else:
            self.twoNameEntry.config(state='normal')
            self.twoNameEntry.delete(0, 'end')
        self.twoNameEntry.config(state='disabled')

    def exit(self):
        self.master.destroy()
