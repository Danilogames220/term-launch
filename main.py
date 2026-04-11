import curses
import os
from enum import Enum
import asyncio
from re import search
import subprocess

from settings import *

class App:
    name = ""
    path = ""
    ex_cmd = ""

    is_hidden = False
    is_terminal = False

    def __init__(self, path):
        self.path = path

        with open(path) as f:
            for line in f:
                # find app name
                if (line.find("Name=") != -1):
                    self.name = line.split("Name=")[1]
               
                # find app launch command
                if (line.find("Exec=") != -1):
                    self.ex_cmd = line.split("Exec=")[1]

                # check if app is hidden 
                if (line.find("NoDisplay=true") != -1 or
                    line.find("Hidden=true") != -1
                ):
                    self.is_hidden = True
                
                # check if it's a terminal app
                if (line.find("Terminal=") != -1) and (line.split("Terminal=")[1] == "true"):
                    self.is_terminal = True
                


class modes(Enum):
    SEARCH = 0
    NAVIGATE = 1

# --- GLOBAL VARIABLES --- #
current_mode = modes.SEARCH

# app list stuff
apps = []
asearch = ""
acount = 0
current_i = 0


c_width = 0
c_height = 0

# --- FUNCTIONS --- #
def close(stdscr):
    exit(0)


# get system apps
def get_apps(dirs):
    files = [] 

    for d in dirs:
        try:
            for f in os.listdir(d):
                files.append(d + f)
        except:
            continue
    
    apps = []
    
    for p in files:
        app = App(p)
        if (not app.is_hidden):
            apps.append(app)

    return apps

# read user input
def usr_in(stdscr):
    global current_mode, current_i
    global asearch

    k = stdscr.getch()
    kb = keybinds
    # quit
    if k == kb.get("quit"):
        close(stdscr)
            
    # confirm
    if k == kb.get("confirm"):
        subprocess.run((apps[current_i].ex_cmd+ " &").split())
        #launch()
        close(stdscr)

    # change modes
    if k == kb.get("switch-mode"):
        stdscr.addstr(7, 0, "switch")

        if current_mode == modes.SEARCH:
            current_mode = modes.NAVIGATE
        else:
            current_mode = modes.SEARCH

# navigation
    # down
    if (k == ord("k") and current_mode == modes.NAVIGATE):
        current_i = (current_i - 1) % acount
        pass
    # up
    if (k == ord("j") and current_mode == modes.NAVIGATE):
        current_i = (current_i + 1) % acount
        pass

    # scroll down
    # scroll up

# navigation - search
            # down
            # up

    #stdscr.addstr(8, 0, "         ")
    stdscr.addstr(8, 0, str(k))

def app_list(stdscr):
    global apps
    global acount

    apps = get_apps(paths)
    
    acount = len(apps)
    
    aoffset = 0

    stdscr.addstr(1, 0, f"{c_width}, {c_height}")


    # print to terminal 
    for i in range(c_height - 2 + aoffset):
        I = i + aoffset # actual app index
        
        if (I == current_i):
            stdscr.addstr(i + 1, 0, f"{apps[I].name}", 
                          curses.A_REVERSE | curses.A_BOLD)
        else:
            stdscr.addstr(i + 1, 0, f"{apps[I].name}")
        pass

# draw search line
def search_line(stdscr):
    if (current_mode == modes.SEARCH):
        stdscr.addstr(0, 0, " Search: ", curses.A_BOLD)
    elif (current_mode == modes.NAVIGATE):
        stdscr.addstr(0, 0, "󰆾 Navigate", curses.A_BOLD)


def main(stdscr):
    global c_width
    global c_height
    c_height, c_width = stdscr.getmaxyx()

    curses.set_escdelay(1) 

    mode = modes.SEARCH
    
    while 1:
        app_list(stdscr)
        search_line(stdscr)
        
        usr_in(stdscr)

curses.wrapper(main)
