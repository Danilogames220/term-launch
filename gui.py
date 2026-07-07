import curses

from public import *
from buffer import *
from entries import *

# handles gui
class Gui:
    window: Win_data
    # NOTE: this should be the only object to have direct acess to the other ones
    buffer: Buffer
    entries: Entries
    
    def clearln(self,
        pos: int, 
    ) -> None:
        self.window.p.addstr(pos, 0, ' ' * (self.window.width - 1))
    def setLn(self,
              line: int,
              row: int,
              text: str,
              curses_style: int = curses.A_NORMAL
    ) -> None:
        self.window.p.addstr(line, row, text, curses_style)

    # search line mode styles
    def sl_search(self, 
        target: str
    ) -> None:
        self.clearln(0)
        t: str = " Search: "
        self.setLn(0, 0, " Search:", curses.A_BOLD | curses.A_UNDERLINE)
        self.setLn(0, len(t), f"{target}")
    def sl_navigate(self,
        target: str
    ) -> None:
        self.clearln(0)
        self.setLn(0, 0, "󰆾 Navigate", curses.A_BOLD| curses.A_UNDERLINE)
        ''' # for debug
        self.window.addstr(0, 0, 
            f"term: {self.entries.apps[self.buffer.pos].is_terminal} " +
            f"path: {self.entries.apps[self.buffer.pos].path} "
        )
        '''

    sl_modes: dict[modes, callable] = {
        modes.SEARCH: sl_search,
        modes.NAV: sl_navigate,
    };

    # draw search line
    def search_line(self,
            target: str
    ) -> None:
        self.sl_modes[self.buffer.mode](self=self, target="target")
    
    # show entry list
    def entry_list(self) -> None:
        lsize: int = self.window.height

        for I in range(1, lsize):
            # actual index
            #i: int = self.el_offset + I - 1
            i: int = self.buffer.cpos + I - 1
            
            self.clearln(I)
            try:
                if (self.buffer.pos == i):
                    self.setLn(I, 0, f"{self.entries.apps[i].name}", curses.A_REVERSE | curses.A_BOLD)
                else:
                    self.setLn(I, 0, f"{self.entries.apps[i].name}")
                continue
            except Exception as e:
                if (e == IndexError):
                    self.clearln(I)
                    self.setLn(I, 0, "~")
                pass
    
    def draw(self) -> None:
        # draw parts of the gui
        self.search_line("search")
        self.entry_list()

        #self.buffer.loop()
    
    def __init__(self, 
        dat: Win_data,
        buf: Buffer,
        ent: Entries,
    ) -> None:
        self.window = dat
        self.buffer = buf
        self.entries = ent
        
