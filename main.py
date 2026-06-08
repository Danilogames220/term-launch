import curses
from enum import Enum
import os

#from settings import *
from gui import *
from public import *


class Input:
    #strscr: curses.window = None
    pass


def main(window: curses.window) -> None:
    
    Gui(window)

curses.wrapper(main)
