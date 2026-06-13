import curses
import threading
# files
from gui import *
from public import *
from buffer import *

class Window:
    gui: Gui
    buffer: Buffer

    def loop(self: Window) -> None:
        pass
    
    def __init__(self: Window, window: curses.window) -> None:
        self.buffer = Buffer(window)
        self.gui = Gui(window, self.buffer)
        
        #gui_t: threading.Thread = threading.Thread(target=self.gui.loop)
        #buffer_t: threading.Thread = threading.Thread(target=self.buffer.loop)
        #gui_t.start()
        #buffer_t.start()
        self.gui.loop()

def main(win: curses.window) -> None:
    cwin: Window = Window(win)   

curses.wrapper(main)
