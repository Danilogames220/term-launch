import curses
# files
from public import *
from gui import *
from buffer import *
from entries import *

class Window:
    data: Win_data

    gui: Gui;
    buffer: Buffer;
    entries: Entries;
    
    def __init__(self, 
        window: curses.window
    ) -> None:
        curses.set_escdelay(1) # get esc press intantly
        curses.curs_set(0) # hide terminal cursor

        self.data = Win_data(window)

        self.entries = Entries()

        self.buffer = Buffer(window, self.entries)
        self.gui = Gui(self.data, self.buffer, self.entries)
        
        self.gui.loop()

def main(win: curses.window) -> None:
    cwin: Window = Window(win)

curses.wrapper(main)
