import curses

from public import *
from entries import *

class Buffer:
    window: curses.window;
    # curent data search string
    data: str = '';
    # buffer mode
    mode: int = modes.SEARCH;
    # cursor pos
    pos: int = 1;
    # maximum cursor pos
    pos_max: int;
    
    # keybinds are set inside __init__
    # first int is the mode for that keybind to trigger
    # second int is for key ascii code
    keybinds: dict[int, dict[int, callable]]; 

    # move cursor pos in the list
    def move_up(self) -> None:
        self.pos = clamp(self.pos + 1, self.pos_max + 1);
    def move_down(self) -> None:
        self.pos = clamp(self.pos + 1, self.pos_max + 1);
    # move list offset only
    '''
    def move_c_up() -> None:
        pass
    def move_c_down() -> None:
        pass
    '''
    # NOTE: only works like this because it only has 2 modes
    def change_mode(self) -> None:
        self.mode = int(not self.mode)
    def term(self) -> None:
        exit(0)
        pass
    def select(self) -> None:
        exit(1)

    # handles input for seach data
    def s_data(self, win: curses.window) -> str:
        return ""

    # handles keypress
    def parse_keypress(self) -> None:
        # current key pressed
        k: int = self.window.getch()
        #self.window.addstr(4, 0, f"{chr(k)}: {k}    ")

        try:
            # NOTE: for some reason it wont run the dict functions unless i have Exception in except
            self.keybinds[self.mode][k]()
        except Exception as e: 
            pass
            #self.window.addstr(3, 0, "e")

    # runs after each time gui draws
    def loop(self) -> None:
        self.parse_keypress()
    
    def __init__(self, win: curses.window) -> None:
        self.window = win
        self.keybinds = {
            modes.SEARCH: {
                ord('q'): self.term,
                ord('e'): self.select
            },
            modes.NAV: {
                ord('q'): self.term,
                ord('e'): self.select
            }
        }; 
        pass

