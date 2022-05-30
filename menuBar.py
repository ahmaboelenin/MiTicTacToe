from tkinter import Menu, messagebox


class MenuBar(Menu):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.infoMenu = Menu(self, tearoff=0)
        self.optionMenu = Menu(self, tearoff=0)

        self.infoMenu.add_command(label="Credits",
                                  command=lambda: messagebox.showinfo("Credits",
                                                                      "This Simple App was Created By Ahmed Aboelenin"))
        self.optionMenu.add_separator()
        self.optionMenu.add_command(label="Exit", command=self.master.destroy)

        self.add_cascade(label="Options", menu=self.optionMenu)
        self.add_cascade(label="Info", menu=self.infoMenu)

        self.master.configure(menu=self)

    def show_option_menu(self, page):
        self.optionMenu.insert_command(0, label="Reset Game", command=page.reset_game)
        self.optionMenu.insert_command(1, label="Back to Main Menu", command=page.return_)

    def hide_option_menu(self):
        self.optionMenu.delete(0, 1)
