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
        self.window.addstr(0, 0, f"mode: {self.buffer.mode}")
    
    # show entry list
    def entry_list(self) -> None:
        # placeholder
        plist: list[str] = [
            "App 0", "App 1", "App 2", "App 3", "App 4",
            "App 5", "App 6", "App 7", "App 8", "App 9",

            "App 10", "App 11", "App 12", "App 13", "App 14",
            "App 15", "App 16", "App 17", "App 18", "App 19",
            
            "App 20", "App 21", "App 22", "App 23", "App 24",
            "App 25", "App 26", "App 27", "App 28", "App 29",
            
            "App 30", "App 31", "App 32", "App 33", "App 34",
            "App 35", "App 36", "App 37", "App 38", "App 39",
        ]

        lsize: int = self.size.y

        for I in range(1, lsize):
            # actual index
            i: int = self.el_offset + I - 1
            
            try:
                if (self.buffer.pos == i):
                    self.window.addstr(I, 0, plist[i], curses.A_BOLD)
                else:
                    self.window.addstr(I, 0, plist[i])
                continue
            except:
                pass
            self.window.addstr(I, 0, "~")
    

    def loop(self) -> None:
        self.is_running = True
        while (self.is_running):
            #self.window.addstr(1, 0, f"w: {self.size.x}; h: {self.size.y}")
        
            # draw parts of the gui
            self.search_line("search")
            self.entry_list()

            self.buffer.loop()
    
    def __init__(self, Window: curses.window, buf: Buffer):
        self.window = Window
        self.buffer = buf
        
        self.size.y, self.size.x = self.window.getmaxyx()

        #self.loop()
        
        pass
