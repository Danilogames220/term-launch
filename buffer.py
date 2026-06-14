import curses

from public import *

class Buffer:
    window: curses.window;

    # curent data search string
    data: str = '';
    # buffer mode
    mode: modes = modes.NAV;
    # cursor pos
    pos: int = 0;
    cpos: int = 0;
    # maximum cursor pos
    pos_max: int;
    
    # keybinds are set inside __init__
    # first int is the mode for that keybind to trigger
    # second int is for key ascii code
    keybinds: dict[modes, dict[int, callable]]; 

    # move cursor pos in the list
    def move_up(self) -> None:
        self.pos = clamp(self.pos + 1, self.pos_max + 1);
    def move_down(self) -> None:
        self.pos = clamp(self.pos - 1, self.pos_max + 1);
    # move list offset only
    def move_c_up(self) -> None:
        self.cpos = clamp(self.cpos + 1, self.pos_max + 1);
    def move_c_down(self) -> None:
        self.cpos = clamp(self.cpos - 1, self.pos_max + 1);
    # NOTE: only works like this because it only has 2 modes
    def change_mode(self) -> None:
        self.mode = modes(not self.mode.value)
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
    
    def __init__(self, 
        win: curses.window,     # window
        e_count: int            # entry count
    ) -> None:
        self.window = win
        self.pos_max = e_count

        self.keybinds = {
            modes.SEARCH: {
                # esc
                27: self.term,
                # ctrl+space
                0: self.change_mode,
                #ord('e'): self.select

                # ctrl-k
                11: self.move_down,
                # ctrl-j
                10: self.move_up,
            },
            modes.NAV: {
                # esc
                27: self.term,
                # ctrl+space
                0: self.change_mode,
                #ord('e'): self.select
                
                # move select
                ord('k'): self.move_down,
                ord('j'): self.move_up,
                # move list offset
                # ctrl-k
                11: self.move_c_down,
                # ctrl-j
                10: self.move_c_up,
            }
        }; 
