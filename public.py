from enum import Enum
import curses

from entries import *

# customize these variables before compiling
# terminal to launch terminal apps
TERMINAL: str = "kitty"
# dirs to pull app entries from
HOMED: str = f"{Path.home()}"
PATHS: list[str] = [
    "/usr/share/applications/",
    "/usr/local/share/applications/",
    f"{HOMED}/.local/share/applications/",
]

# NOTE: if you add aother mode, change how Buffer.change_mode() works
class modes(Enum):
    SEARCH = 0
    NAV = 1

# wrapper for shared window data
class Win_data:
    width: int = -1
    height: int = -1
    p: curses.window # pointer to curses.window

    selected_entry_index: int = 0;
    list_display_offset: int = 0;

    entries: list[App]
    entry_count: int = 0;

    query_target: str = ""
    # for Gui class
    # if it is at the end of the query(as usualy), then its value should be len(query_target)
    query_cursor_pos: int = 0

    mode: modes = modes.NAV

    def set_entries(self,
        List: list[App]
    ) -> None:
        self.entries = List
        self.entry_count = len(List)

    #def set_misc(self) -> None:
    #    self.

    def __init__(self,
        win: curses.window
    ) -> None:
        self.p = win
        self.height, self.width = self.p.getmaxyx()

# keeps a value between x and y
def clamp(n: int, x: int, y: int = 0) -> int:
    if n < x:
        return x
    if n > y:
        return y
    return n
    #return n % x
