# asni color codes
# https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124
import curses
from enum import Enum

from settings import *

class modes(Enum):
    SEARCH = 0
    NAVIGATE = 1
current_mode = 0

apps = []
asearch = ""
aindex = 0

def close(stdscr):
    exit(0)
    '''
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()

    curses.endwin(stdscr)
    '''
    

# get system apps
def get_apps(dirs):
    '''
    apps = [
        "app1",
        "app2",
        "app3",
    ]
    
    app_count = len(apps)
    '''
    return []

# read user input
def usr_in(stdscr, index, mode, buffer):
    #stdscr.nodelay(True)
    while 1:
        usr_key = stdscr.getch()
        
        kb = keybinds
        match(usr_key):
        # quit
            case k if k == kb.get("quit"):
                close(stdscr)
            
        # confirm
            case k if k == kb.get("confirm"):
                launch(buffer)
                close(stdscr)
           
        # change modes
            case k if k == kb.get("switch-mode"):
                stdscr.addstr(7, 0, "buceta")

        # navigation - search
            # down
            case k if k == ord("w"):
                stdscr.addstr(7, 0, "         ")
            # up
        # navigation - move
            # down
            # up

            case _:
                stdscr.addstr(7, 0, str(usr_key))

def app_list(stdscr):
    pass

# draw search line
def search_line(stdscr):
    pass


def main(stdscr):
    curses.set_escdelay(1) 
    apps = [
        "app1",
        "app2",
        "app3",
    ]
    
    app_count = len(apps)
    
    # search line
    stdscr.addstr(0, 0, " Search: ")
    
    # print to terminal 
    for i in range(0, len(apps)):
        if (app_count - 1 - i >= 0):
            stdscr.addstr(i + 1, 0, f"{apps[i]}")

    usr_in(stdscr, 1, None, None)

curses.wrapper(main)
