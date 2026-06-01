# TODO
# > IMPORTANT
# - offset thing
# - make this code less crap
# - config

# > DO LATER
# - icons in kitty terminal

import curses
import os
from enum import Enum
import asyncio
from re import search
import subprocess

from settings import *

class App:
    name: str = ""
    path: str  = ""
    ex_cmd: str = ""

    is_hidden: bool = False
    is_terminal: bool = False

    def __init__(self: App, path: str):
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
apps: list = []
asearch: str = ""
acount: int = 0
aoffset: int = 1

current_i: int = 0

c_width: int = 0
c_height: int = 0

# --- FUNCTIONS --- #
def close(stdscr) -> None:
    exit(0)


# get system apps
def get_apps(dirs) -> list[App]:
    files: list = [] 

    for d in dirs:
        try:
            for f in os.listdir(d):
                files.append(d + f)
        except:
            continue
    
    apps: list = []
    
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
        subprocess.Popen(apps[current_i].ex_cmd.split(),
                         preexec_fn=os.setpgrp)
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
    global acount, aoffset

    apps: list[App] = get_apps(paths)
    
    acount = len(apps)
    
    alimit = c_height - 2

    # TODO
    # print to terminal 
    s_visible = False
    for i in range(alimit):
        
        if (i + aoffset == current_i):
            stdscr.addstr(i + 1, 0, f"{apps[i + aoffset].name}", 
                          curses.A_REVERSE | curses.A_BOLD)
            s_visible = True
        else:
            stdscr.addstr(i + 1, 0, f"{apps[i + aoffset].name}")
        
        if (not s_visible):
            pass

# draw search line
def search_line(stdscr) -> None:
    if (current_mode == modes.SEARCH):
        stdscr.addstr(0, 0, " Search: ", curses.A_BOLD)
    elif (current_mode == modes.NAVIGATE):
        stdscr.addstr(0, 0, "󰆾 Navigate", curses.A_BOLD)


def main(stdscr) -> None:
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
