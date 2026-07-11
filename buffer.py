import curses
import subprocess

from public import *

class Buffer:
    w_data: Win_data;
    window: curses.window;
    entries: Entries;

    # curent data search string
    data: str = "data";
    # maximum cursor pos
    pos_max: int;
    cpos_max: int;
    
    # keybinds are set inside __init__
    # first int is the mode for that keybind to trigger
    # second int is for key ascii code
    keybinds: dict[modes, dict[int, callable]]; 

    # move list offset only
    def move_c_down(self) -> None:
        self.w_data.list_display_offset = clamp(
                self.w_data.list_display_offset + 1, 
                0, self.pos_max + 1
        );
    def move_c_up(self) -> None:
        self.w_data.list_display_offset = clamp(
                self.w_data.list_display_offset - 1, 
                0, self.pos_max + 1
        );
    # move cursor pos in the list
    def move_down(self) -> None:
        self.w_data.selected_entry_index = clamp(
                self.w_data.selected_entry_index + 1, 
        0, self.pos_max);
        # move cpos if cursor goes offscreen
        if (
            self.w_data.selected_entry_index - self.w_data.list_display_offset
            >
            #self.w_data.list_display_offset
            self.cpos_max
        ):
            self.move_c_down() 

    def move_up(self) -> None:
        self.w_data.selected_entry_index = clamp(
                self.w_data.selected_entry_index - 1, 
        0, self.pos_max);
        # move cpos if cursor goes offscreen
        if (
            self.w_data.selected_entry_index 
            < 
            self.w_data.list_display_offset
        ):
            self.move_c_up() 

    # NOTE: only works like this because it only has 2 modes
    def change_mode(self) -> None:
        self.w_data.mode = modes(not self.w_data.mode.value)
    def term(self) -> None:
        exit(0)
        pass
    def select(self) -> None: 
        # selected app
        s_app: App = self.w_data.entries[self.w_data.selected_entry_index]
        exec_cmd: list[str] # s_app.ex_cmd

        if (s_app.is_terminal):
            exec_cmd = [TERMINAL] + s_app.ex_cmd.split()
        else:
            exec_cmd = s_app.ex_cmd.split()

        subprocess.Popen(
            exec_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        ) 
        exit(0)

    # handles input for seach data
    def add_chr(self) -> str:
        return ""

    # handles keypress
    def parse_keypress(self) -> None:
        # current key pressed
        k: int = self.w_data.p.getch()

        try:
            # NOTE: for some reason it wont run the dict functions unless i have Exception in except
            self.keybinds[self.w_data.mode][k]()
        except Exception as e: 
            pass

    # runs after each time gui draws
    # TODO rename this (looping will be handled my window)
    def loop(self) -> None:
        self.parse_keypress()
    
    def __init__(self,
        data: Win_data
    ) -> None:
        self.w_data = data

        self.pos_max = self.w_data.entry_count - 1 # not having this - 1 will draw a enpty entry
        self.cpos_max = self.w_data.height - 2

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
