from tkinter import Label
from itertools import count, cycle
from assets import Image, ImageTk, resource_path


class LoadingPage(Label):
    def __init__(self, master):
        super().__init__(master=master, bg="#FFFFFF", highlightthickness=0)
        self.interrupt = False
        self.delay, self.frames = None, None

        self.init()

        self.pack(expand=1, fill="both")

    def init(self):
        image = Image.open(resource_path(r"assets/loading.gif"))
        frames = []
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(image.copy()))
                image.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = image.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def next_frame(self):
        if self.interrupt:
            self.interrupt = False
            return

        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)
