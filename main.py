# TODO:
# - find a way to compile this
# - add app icon support to terminals that support images
# - config file
# - horizontal cursor movement in search mode
# - fix search text overflow

import curses
# files
from public import *
from gui import *
from buffer import *
from entries import *

import sys
class Win_args:
    paths: list[str] = [
        "/usr/share/applications/",
        "/usr/local/share/applications/",
        f"~/.local/share/applications/",
    ]

    def __init__(self):
        args: list[str] = sys.argv[1:]

        if ("-h" in args) or ("--help" in args):
            print(
f"""Usage: terml [Options]
-p --paths   Directories to look for apps (dir1;dir2;dir3;...)

When no options are specified, the defaults are:
paths:""")
            for p in self.paths:
                print(p)

            print("""
Source code:
<https://github.com/danilogames220/term-launch>""")
            exit(0)
        
        # position of the flags in args
        t_pos: int = -1
        d_pos: int = -1
        for arg in args:
            if (arg == "-p") or (arg == "--paths"):
                pass
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
    args: Win_args

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
        win: curses.window,
        args: Win_args
    ) -> None:
        curses.set_escdelay(1) # no esc press delay
        
        self.args = args
        self.init_objects(win)
        
        self.loop()

# get arguments before starting window so that the program can print -h or other stuff without starting
arguments: Win_args = Win_args()
curses.wrapper(lambda win: Window(win, arguments))
