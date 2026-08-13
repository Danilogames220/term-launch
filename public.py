from enum import Enum
import curses

#from entries import *

# NOTE: if you add aother mode, change how Buffer.change_mode() works
class modes(Enum):
    SEARCH = 0
    NAV = 1

# Holds data of each app
class App:
    name: str;
    path: str;
    raw_cmd: str;

    ex_cmd: str = "";
    is_hidden: bool = False
    is_terminal: bool = False
    
    def parse_cmd(self, 
        cmd: str
    ) -> str:
        p_cmd: str = cmd

        p_cmd = p_cmd.replace("%f", "")
        p_cmd = p_cmd.replace("%F", "")
        p_cmd = p_cmd.replace("%u", os.getcwd())
        p_cmd = p_cmd.replace("%U", "")
        p_cmd = p_cmd.replace("%i", "")
        p_cmd = p_cmd.replace("%", "") # keep this one at last to not mess up the others

        return p_cmd
    

    def __init__(self, path: str):
        self.path = path
        self.name = ""
        
        with open(path) as f:
            def check(l: str, arg: str) -> bool:
                return (l.find(arg) != -1)

            for line in f:
                # find app name
                if (check(line, "Name=")) and (len(self.name) == 0):
                    self.name = line.split("Name=")[1]
                    #self.name = line[line.find("Name="):]
                # find app launch command
                if (check(line, "Exec=")) and (self.ex_cmd == ""):
                    self.ex_cmd = line.split("Exec=")[1]

                # check if app is hidden 
                if (check(line, "NoDisplay=true")) or (check(line, "Hidden=true")):
                    self.is_hidden = True
                
                # check if it is a terminal app
                if (check(line, "Terminal=true")):
                    self.is_terminal = True

# wrapper for shared window data
class Win_data:
    width: int = -1
    height: int = -1
    p: curses.window 

    selected_entry_index: int = 0;
    list_display_offset: int = 0;

    entries: list[App]
    entry_count: int = 0;

    query_target: str = ""
    # for Gui class
    # horizontal position of the cursor when typing in search mode
    # query_cursor_pos: int = 0

    mode: modes = modes.SEARCH

    terminal: str;
    #paths: list[str];

    def set_entries(self,
        List: list[App]
    ) -> None:
        self.entries = List
        self.entry_count = len(List)

    def __init__(self,
        win: curses.window,
        term: str
    ) -> None:
        self.p = win
        self.terminal = term
        self.height, self.width = self.p.getmaxyx()
        

# keeps a value between x and y
def clamp(n: int, x: int, y: int = 0) -> int:
    if n < x:
        return x
    if n > y:
        return y
    return n
