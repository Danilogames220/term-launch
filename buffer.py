import curses
import subprocess

from public import *

class Buffer:
    w_data: Win_data;
    window: curses.window;
    entries: Entries;

    # string to search apps
    data: str = "";
    # maximum cursor position
    pos_max: int;
    cpos_max: int;
    
    # NOTE: keybinds can only be set inside __init__
    # modes: the mode where the keybind can trigger
    # dict.int: key value
    # dict.callable: function to trigger
    keybinds: dict[modes, dict[int, callable]]; 

    # moves entry list offset
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
    # moves selected entry
    def move_down(self) -> None:
        self.w_data.selected_entry_index = clamp(
                self.w_data.selected_entry_index + 1, 
        0, self.pos_max);
        # move cpos if cursor goes offscreen
        if (
            self.w_data.selected_entry_index - self.w_data.list_display_offset
            >
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
        exec_cmd: list[str] = s_app.ex_cmd.split()
        
        if (s_app.is_terminal):
            subprocess.run(
                exec_cmd
                #stdout=subprocess.DEVNULL,
                #stderr=subprocess.STDOUT
            )
        else:
            subprocess.Popen(
                exec_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT
            ) 
        exit(0)

    # handles input for seach data
    def add_chr(self, k: int) -> None:
        if (32 <= k <= 125):
            self.data += chr(k)
        
        if (k == 263):
            self.data = self.data[:-1]
        self.w_data.query_target = self.data

    # handles keypress
    def parse_keypress(self) -> None:
        # current key pressed
        k: int = self.w_data.p.getch()
        
        # get keys between [32...125] to add to data
        if (self.w_data.mode == modes.SEARCH):
            self.add_chr(k)
        try:
            # NOTE: for some reason it wont run the dict functions unless it catches the exception 
            self.keybinds[self.w_data.mode][k]()
        except Exception as e: 
            pass

    # runs after each time gui draws
    def loop(self) -> None:
        self.parse_keypress()
    
    def __init__(self,
        data: Win_data
    ) -> None:
        self.w_data = data

        self.pos_max = self.w_data.entry_count - 1 # not having this - 1 will draw a empty entry
        self.cpos_max = self.w_data.height - 2

# ----- KEYBINDS ----- #
        self.keybinds = {
            modes.SEARCH: {
                # esc
                27: self.term,
                # ctrl+space
                0: self.change_mode,
                # select
                10: self.select,
                
                # move with arrow keys
                258: self.move_down,
                259: self.move_up,
                336: self.move_c_down,
                337: self.move_c_up,
            },
            modes.NAV: {
                # esc
                27: self.term,
                # ctrl+space
                0: self.change_mode,
                # select
                10: self.select,
                
                # move select
                ord('j'): self.move_down,
                ord('k'): self.move_up,
                # move list offset
                ord('J'): self.move_c_down,
                ord('K'): self.move_c_up,
                
                # move with arrow keys
                258: self.move_down,
                259: self.move_up,
                336: self.move_c_down,
                337: self.move_c_up,

            }
        }; 
