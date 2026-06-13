import curses

from public import *
from buffer import *

# handles gui
class Gui:
    # window
    window: curses.window
    # pointer to window buffer
    buffer: Buffer
    # list of each app entry
    apps: list[App]
    is_running: bool = False
    
    # window size
    size: vec2 = vec2(-1, -1)
    
    # entry list offset
    el_offset: int;

    # show search line
    def search_line(
            self: Gui,
            target: str
    ) -> None:
        self.window.addstr(0, 0, target)
    
    # show entry list
    def entry_list() -> None:
        pass
    

    def loop(self: Gui) -> None:
        #self.window.addstr(1, 0, f"w: {self.size.x}; h: {self.size.y}")
        
        # draw parts of the gui
        self.search_line("search")
        #self.entry_list()
            
        if (self.window.getch() == ord('q')):
            exit(0)

    
    def __init__(self: Gui, Window: curses.window):
        self.window = Window
        
        self.size.y, self.size.x = self.window.getmaxyx()

        self.is_running = True
        while (self.is_running):
            self.loop()
        
        pass
