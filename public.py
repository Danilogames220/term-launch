from enum import Enum
import curses

from entries import *

# NOTE: if you add aother mode, change how Buffer.change_mode() works
class modes(Enum):
    SEARCH = 0
    NAV = 1

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
