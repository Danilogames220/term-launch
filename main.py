import curses
# files
from public import *
from gui import *
from buffer import *
from entries import *

class Window:
    gui: Gui;
    buffer: Buffer;
    entries: Entries;

    #def term(self) -> None:
    #    pass
    
    def __init__(self, 
        window: curses.window
    ) -> None:
        curses.set_escdelay(1)

        self.entries = Entries()

        self.buffer = Buffer(window, self.entries)
        self.gui = Gui(window, self.buffer, self.entries)
        
        self.gui.loop()

def main(win: curses.window) -> None:
    cwin: Window = Window(win)   

curses.wrapper(main)
