import curses

from public import *

# handles gui
class Gui:
    window: curses.window
    is_running: bool = False
    
    # window size
    size: vec2 = vec2(-1, -1)
    
    def search_line(
            self: Gui,
            target: str
    ) -> None:
        self.window.addstr(0, 0, target)

    def entry_list(apps: list[App]):
        pass
    

    def loop(self: Gui) -> None:
        while (self.is_running):
            self.search_line("search")
            
            if (self.window.getch() == ord('q')):
                exit(0)


    
    def __init__(self: Gui, Window: curses.window):
        self.window = Window
        
        self.is_running = True
        self.loop()
        
        pass
