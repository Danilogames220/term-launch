import curses

from public import *

class Buffer:
    # curent data search string
    data: str;
    # buffer mode
    mode: int;
    # cursor pos
    pos: int;
    # maximum cursor pos
    pos_max: int;
    
    # move cursor pos in the list
    def move_up() -> None:
        pass
    def move_down() -> None:
        pass
    # move list offset only
    '''
    def move_c_up() -> None:
        pass
    def move_c_down() -> None:
        pass
    '''
    def change_mode() -> None:
        pass
    def quit() -> None:
        pass
    # handles input for seach data
    def s_data(self: Input, win: curses.window) -> str:
        return ""

    def loop() -> None:
        pass
    
    def __init__() -> None:

