import curses
import subprocess

from public import *
from entries import *

class Buffer:
    w_data: Win_data;
    window: curses.window;
    entries: Entries;

    # curent data search string
    data: str = "data";
    # buffer mode
    mode: modes = modes.NAV;
    # current app selected of self.entries
    pos: int = 0;
    cpos: int = 0;
    # maximum cursor pos
    pos_max: int;
    cpos_max: int;
    
    # keybinds are set inside __init__
    # first int is the mode for that keybind to trigger
    # second int is for key ascii code
    keybinds: dict[modes, dict[int, callable]]; 

    # move list offset only
    def move_c_down(self) -> None:
        self.cpos = clamp(self.cpos + 1, 0, self.pos_max + 1);
    def move_c_up(self) -> None:
        self.cpos = clamp(self.cpos - 1, 0, self.pos_max + 1);
    # move cursor pos in the list
    def move_down(self) -> None:
        self.pos = clamp(self.pos + 1, 0, self.pos_max);
        # move cpos if cursor goes offscreen
        if (
            self.pos - self.cpos
            >
            self.cpos_max
            #self.cpos_max
        ):
            self.move_c_down() 

    def move_up(self) -> None:
        self.pos = clamp(self.pos - 1, 0, self.pos_max);
        # move cpos if cursor goes offscreen
        if (
            self.pos 
            < 
            self.cpos
        ):
            self.move_c_up() 

    # NOTE: only works like this because it only has 2 modes
    def change_mode(self) -> None:
        self.mode = modes(not self.mode.value)
    def term(self) -> None:
        exit(0)
        pass
    def select(self) -> None: 
        # selected app
        s_app: App = self.w_data.entries[self.pos]
        #s_app: App = self.w_data.entries[self.w_data.selected_entry_index]
        #s_app: App = self.entries.apps[self.pos]
        exec_cmd: list[str] # s_app.ex_cmd
        
        #TERMINAL: str = "kitty"

        if (s_app.is_terminal):
            exec_cmd = [TERMINAL] + s_app.ex_cmd.split()
        else:
            exec_cmd = s_app.ex_cmd.split()

        subprocess.Popen(
            exec_cmd, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ) 
        exit(0)

    # handles input for seach data
    def add_chr(self) -> str:
        return ""

    # handles keypress
    def parse_keypress(self) -> None:
        # current key pressed
        k: int = self.window.getch()

        try:
            # NOTE: for some reason it wont run the dict functions unless i have Exception in except
            self.keybinds[self.mode][k]()
        except Exception as e: 
            pass

    # runs after each time gui draws
    # TODO rename this (looping will be handled my window)
    def loop(self) -> None:
        self.parse_keypress()
    
    def __init__(self,
        data: Win_data,
        win: curses.window,     # window
        #ent: Entries            # entries pointer
    ) -> None:
        self.w_data = data
        self.window = win
        #self.entries = ent

        self.pos_max = self.w_data.entry_count - 1 # not having this - 1 will draw a enpty entry
        self.cpos_max = self.w_data.height - 2  #win.getmaxyx()[0] - 2

        self.keybinds = {
            modes.SEARCH: {
                # esc
                27: self.term,
                # ctrl+space
                0: self.change_mode,
                # select
                10: self.select,
            },
            modes.NAV: {
                # esc
                27: self.term,
                # ctrl+space
                0: self.change_mode,
                #ord('e'): self.select
                
                # move select
                ord('j'): self.move_down,
                ord('k'): self.move_up,
                # move list offset
                ord('J'): self.move_c_down,
                ord('K'): self.move_c_up,

                # select
                10: self.select,
            }
        }; 
