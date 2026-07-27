# TODO:
# - find a way to compile this
# - add app icon support to terminals that support images
# - config file
# - horizontal cursor movement in search mode
# - fix search text overflow

import curses
#from os import 
import sys
from pathlib import Path
# files
from public import *
from gui import *
from buffer import *
from entries import *

# This could have its own file
class Win_args:
    paths: list[str] = [
        "/usr/share/applications/",
        "/usr/local/share/applications/",
        "~/.local/share/applications/",
    ]
    terminal: str = ""

    def __init__(self):
        args: list[str] = sys.argv[1:]

        if (args == []):
            return

        if ("-h" in args) or ("--help" in args):
            print(
f"""Usage: terml [Options]
-t= --terminal=  Launch terminal apps in a new terminal window. 
                 if =NULL or unset, terminal apps will launch 
                 on the same terminal that the program ran.
-p --paths       Directories to look for apps (dir1/;dir2/;dir3/;...).
                 You can't use "./" in the paths

When paths are not specified, the defaults are:""")
            for p in self.paths:
                print(p)

            print("""
Source code:
<https://github.com/danilogames220/term-launch>""")
            sys.exit(0)
        
        # get dirs passed by the user
        p_pos: int = 0
        for arg in args:
            # handle terminal flag
            if ("-t=" in arg):
                self.terminal = arg.replace("-t=", "")
            if ("--terminal=" in arg):
                self.terminal = arg.replace("--terminal=", "")

            if (arg == "-p") or (arg == "--paths"):
                break
            p_pos += 1
        try:
            if ("-p" in args) or ("--paths" in args):
                self.paths = args[p_pos + 1].split(";")
        except Exception as e:
            if (type(e) != IndexError):
                raise e
            print("ERROR: No paths provided")
            sys.exit(0)
        
        # replace ~ with home dir
        if (self.terminal == "NULL"):
            self.terminal = ""
        t_paths: list[str] = []
        for p in self.paths:
            t_paths.append(p.replace("~", f"{Path.home()}"))
        self.paths = t_paths
        
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
        self.data = Win_data(window, self.args.terminal)

        self.entries = Entries(self.data, self.args.paths)
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
