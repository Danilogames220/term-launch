import curses
from enum import Enum
import os

#from settings import *
from gui import *
from public import *
from buffer import *

class Window:
    gui: Gui
    buffer: Buffer

    def __init__(self: Window, window: curses.window) -> None:
        self.gui = Gui(window)

    def loop(self: Window) -> None:
        pass

def main(win: curses.window) -> None:
    cwin: Window = Window(win)   

curses.wrapper(main)
