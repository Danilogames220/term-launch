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

        self.entries = Entries(self.data, PATHS)
        # set data variables
        self.data.set_entries(self.entries.apps)
        #self.data
        self.buffer = Buffer(self.data)

        self.gui = Gui(self.data)

    # to avoid conflits with each object, the window will organize what each object will do when a new seach is done by the user
    # store last search text so that when the app list resizes, the current pos isn't at somewhere it shoudn't be
    last_search: str = ""
    def new_query(self) -> None:
        text: str = self.buffer.data # get text
        if (text.upper() != self.last_search.upper()):
            self.data.selected_entry_index = 0
            self.data.list_display_offset = 0
        
        self.data.set_entries(self.entries.filter(text))
        self.last_search = text

    def loop(self) -> None:
        self.is_running = True
        while (self.is_running):
            # filter
            self.new_query()
            # draw screen
            self.gui.draw()
            # get input
            self.buffer.loop()

    def __init__(self, 
        win: curses.window
    ) -> None:
        curses.set_escdelay(1) # get esc press intantly
        
        self.init_objects(win)
        
        self.loop()

def main(win: curses.window) -> None:
    Window(win)

curses.wrapper(main)
