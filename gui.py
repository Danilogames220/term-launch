import curses

from public import *
from buffer import *
from entries import *

# handles gui
class Gui:
    # window
    window: curses.window
    # pointer to window buffer
    buffer: Buffer
    # pointer to window entries
    entries: Entries

    # list of each app entry
    apps: list[App]
    is_running: bool = False
    
    # window size
    size: vec2 = vec2(-1, -1)
    
    # entry list offset
    el_offset: int = 0;

    # show search line
    def search_line(
            self: Gui,
            target: str
    ) -> None:
        self.window.addstr(0, 0, f"mode: {self.buffer.mode}; pos = {self.buffer.pos}    ")
    
    # show entry list
    def entry_list(self) -> None:
        # placeholder
        plist: list[str] = self.entries.plist

        lsize: int = self.size.y

        for I in range(1, lsize):
            # actual index
            #i: int = self.el_offset + I - 1
            i: int = self.buffer.cpos + I - 1
            
            try:
                if (self.buffer.pos == i):
                    self.window.addstr(I, 0, f"{plist[i]}         ", curses.A_REVERSE | curses.A_BOLD)
                else:
                    self.window.addstr(I, 0, f"{plist[i]}         ")
                continue
            except:
                pass
            self.window.addstr(I, 0, "~                                       ")
    

    def loop(self) -> None:
        self.is_running = True
        while (self.is_running):
            #self.window.addstr(1, 0, f"w: {self.size.x}; h: {self.size.y}")
        
            # draw parts of the gui
            self.search_line("search")
            self.entry_list()

            self.buffer.loop()
    
    def __init__(self, 
        Window: curses.window, 
        buf: Buffer,
        ent: Entries
    ) -> None:
        self.window = Window
        self.buffer = buf
        self.entries = ent
        
        self.size.y, self.size.x = self.window.getmaxyx()

        #self.loop()
        
        pass
