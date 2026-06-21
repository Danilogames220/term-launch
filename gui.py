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

    def clearln(self,
        pos: int, 
    ) -> None:
        self.window.addstr(pos, 0, ' ' * (self.size.x - 1))

    # search line mode styles
    def sl_search(self, 
        target: str
    ) -> None:
        self.clearln(0)
        t: str = " Search: "
        self.window.addstr(0, 0, " Search:", curses.A_BOLD | curses.A_UNDERLINE)
        self.window.addstr(0, len(t), f"{target}")
    def sl_navigate(self,
        target: str
    ) -> None:
        self.clearln(0)
        # TODO change this
        #self.window.addstr(0, 0, "󰆾 Navigate", curses.A_BOLD| curses.A_UNDERLINE)
        self.window.addstr(0, 0, 
            f"cpos_max: {self.buffer.cpos_max} " + 
            f"pos: {self.buffer.pos}"
        )

    sl_modes: dict[modes, callable] = {
        modes.SEARCH: sl_search,
        modes.NAV: sl_navigate,
    };

    # draw search line
    def search_line(self,
            target: str
    ) -> None:
        #self.window.addstr(0, 0, f"mode: {self.buffer.mode}; pos = {self.buffer.pos}    ")
        self.sl_modes[self.buffer.mode](self=self, target="target")
    
    # show entry list
    def entry_list(self) -> None:
        lsize: int = self.size.y

        for I in range(1, lsize):
            # actual index
            #i: int = self.el_offset + I - 1
            i: int = self.buffer.cpos + I - 1
            
            self.clearln(I)
            try:
                if (self.buffer.pos == i):
                    self.window.addstr(I, 0, f"{self.entries.apps[i].name}", curses.A_REVERSE | curses.A_BOLD)
                else:
                    self.window.addstr(I, 0, f"{self.entries.apps[i].name}")
                continue
            except Exception as e:
                #self.clearln(I)
                #self.window.addstr(I, 0, f"~ {e}")
                pass
    

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
