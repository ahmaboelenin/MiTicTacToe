from threading import Thread
from PIL import Image, ImageTk
from time import sleep


class ThreadedTask(Thread):
    def __init__(self, target, args=None):
        super().__init__(target=target, args=(args,))
        self.start()


def resource_path(relative_path):
    import os
    import sys
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
