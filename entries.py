import os
from pathlib import Path

from public import *


# Holds data of each app
class App:
    name: str;
    path: str;
    raw_cmd: str;

    ex_cmd: str;
    is_hidden: bool = False
    is_terminal: bool = False
    
    def parse_cmd(self, 
        cmd: str
    ) -> str:
        p_cmd: str = cmd

        return p_cmd
    
    '''
    # functions to do for each thing found
    def p_name(self, l: str) -> Bool:
        return True
    def p_hidden(self, l: str) -> Bool:
        return True
    def p_exec(self, l: str) -> Bool:
        return True

    def parse_file(self,
        path: str
    ) -> None:
        for line in path:
            try:
                pass
            except:
                pass
        pass
    '''

    def __init__(self, path: str):
        self.path = path
        self.name = ""

        raw_cmd: str = ""
        
        with open(path) as f:
            def check(l: str, arg: str) -> bool:
                return (l.find(arg) != -1)

            for line in f:
                # find app name
                if (check(line, "Name=")) and (len(self.name) == 0):
                    self.name = line.split("Name=")[1]
                    #self.name = line[line.find("Name="):]
                # find app launch command
                if (check(line, "Exec=")):
                    self.ex_cmd = self.parse_cmd(line.split("Exec=")[1])

                # check if app is hidden 
                if (check(line, "NoDisplay=true")) or (check(line, "Hidden=true")):
                    self.is_hidden = True
                
                # check if it is a terminal app
                if (check(line, "Terminal=true")):
                    self.is_terminal = True

# handles apps
class Entries:
    # all visible apps
    apps: list[App]
    # filtered apps
    filtered_apps: list[App]

    
    # TODO: make this get all entries at the same time
    def get(self) -> list[App]:
        homed: str = f"{Path.home()}"
        paths: list[str] = [
            "/usr/share/applications/",
            "/usr/local/share/applications/",
            f"{homed}/.local/share/applications/",
        ]

        files: list = []; 
        for d in paths:
            try:
                for f in os.listdir(d):
                    files.append(d + f)
            except:
                continue
    
        apps: list[App] = []
    
        for p in files:
            # check if is a .desktop file
            ext: str = "desktop"
            if not (p[len(p) - len(ext):] == ext):
                    continue
            
            # check if is a hidden entry
            a_temp: App = App(p)
            if (not a_temp.is_hidden):
                apps.append(a_temp)
        
        return apps
    def search(self) -> None:
        pass

    def __init__(self) -> None:
        self.apps = self.get()
        pass
