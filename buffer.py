import curses
import os
import subprocess

from public import *
from entries import *

class Buffer:
    window: curses.window;
    entries: Entries;

    # curent data search string
    data: str = "data";
    # buffer mode
    mode: modes = modes.NAV;
    # cursor pos
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
        self.cpos = clamp(self.cpos + 1, 0, self.cpos_max + 1);
    def move_c_up(self) -> None:
        self.cpos = clamp(self.cpos - 1, 0, self.cpos_max + 1);
    # move cursor pos in the list
    def move_down(self) -> None:
        '''
        if (
            self.pos - self.cpos - 1 
            < 
            self.cpos_max
        ):
            self.pos = self.cpos
            return
        '''
        self.pos = clamp(self.pos + 1, 0, self.pos_max);
        # move cpos if cursor goes offscreen
        if (
            self.pos - self.cpos - 1
            > 
            self.cpos_max
        ):
            self.move_c_down() 

    def move_up(self) -> None:
        '''
        if (
            self.pos - self.cpos - 1 
            > 
            self.cpos_max
        ):
            self.pos = self.cpos + self.cpos_max
            return
        '''
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
        '''
        subprocess.Popen(
            self.entries.apps[self.pos].ex_cmd.split(),
            preexec_fn=os.setpgrp
        )
        '''
        subprocess.Popen('kitty -c "zsh"'.split(), stdout=subprocess.PIPE) 
        exit(1)

    # handles input for seach data
    def add_chr(self) -> str:
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
        ent: Entries,           # entries pointer
        e_count: int            # entry count
    ) -> None:
        self.window = win
        self.entries = ent

        self.pos_max = e_count 
        self.cpos_max = e_count - win.getmaxyx()[0] + 1

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
                ord('j'): self.move_down,
                ord('k'): self.move_up,
                # move list offset
                ord('J'): self.move_c_down,
                ord('K'): self.move_c_up,

                # select
                10: self.select,
            }
        }; 
