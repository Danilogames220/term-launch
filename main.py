import curses
# files
from public import *
from gui import *
from buffer import *
from entries import *

# NOTE:
# - Things that require managing multiple objects at once (like filtering apps, etc...) should be done by the window. This is to make the code better to manage
# 
# * App loop:
# - process apps (get / filter)
# - draw stuff
# - get new input
# - repeat
class Window:
    data: Win_data

    gui: Gui;
    buffer: Buffer;
    entries: Entries;

    is_running: bool = False;
    
    def init_objects(self,
        window: curses.window
    ) -> None:
        self.data = Win_data(window)

        self.entries = Entries(self.data)
        # set data variables
        self.data.set_entries(self.entries.apps)
        #self.data


        self.buffer = Buffer(self.data)

        self.gui = Gui(self.data, self.buffer, self.entries)

    # to avoid conflits with each object, the window will organize what each object will do when a new seach is done by the user
    def new_query(self) -> None:
        # - text from buffer is passed to entries
        # - entries filters the apps
        # - entries returns the filtered apps to win_data
        # > do this then draw the screen
        #
        # text: str = self.buffer.get_text() # get text
        # self.entries.filter(text)
        # data.set_entries(self.entries.filtered_apps)
        
        pass
    
    def loop(self) -> None:
        self.is_running = True
        while (self.is_running):
            # draw screen
            self.gui.draw()
            # get input
            self.buffer.loop()

    def __init__(self, 
        win: curses.window
    ) -> None:
        curses.set_escdelay(1) # get esc press intantly
        curses.curs_set(0)     # hide terminal cursor
        
        self.init_objects(win)
        
        self.loop()

def main(win: curses.window) -> None:
    Window(win)

curses.wrapper(main)
