import curses

from public import *
#from entries import *

# handles gui
class Gui:
    window: Win_data
    # NOTE: this should be the only object to have direct acess to the other ones
    
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
    

# ----- SEACH LINE ----- #
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
        #self.setLn(0, 0, f"cmd = {self.window.entries[self.window.selected_entry_index].ex_cmd}")

    sl_modes: dict[modes, callable] = {
        modes.SEARCH: sl_search,
        modes.NAV: sl_navigate,
    };

    # draw search line
    def search_line(self,
            target: str
    ) -> None:
        self.sl_modes[self.window.mode](self=self, target="target")


# ----- ENTRY LIST ----- #
    # show entry list
    def entry_list(self) -> None:
        lsize: int = self.window.height

        for I in range(1, lsize):
            # actual index
            i: int = self.window.list_display_offset + I - 1
            
            self.clearln(I)
            try:
                entry: list[App] = self.window.entries
                if (self.window.selected_entry_index == i):
                    self.setLn(I, 0, f"{entry[i].name}", curses.A_REVERSE | curses.A_BOLD)
                else:
                    self.setLn(I, 0, f"{entry[i].name}")
                continue
            except Exception as e:
                if (e == IndexError):
                    self.clearln(I)
                    self.setLn(I, 0, "~")
                pass

# ----- MAIN ----- #
    def draw(self) -> None:
        # draw parts of the gui
        self.search_line("search")
        self.entry_list()
    
    def __init__(self, 
        dat: Win_data
    ) -> None:
        self.window = dat
        
