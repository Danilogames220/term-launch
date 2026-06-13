import curses

class Input:
    # user search
    buffer: str;
    
    mode: int;

    def read(self: Input, win: curses.window) -> str:
        return ""

