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
        return ""
    
    def parse_file(self,
        path: str
    ) -> None:
        pass

    def __init__(self, path: str):
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

# handles apps
class Entries:
    apps: list[App]
    plist: list[str] =  [
        "App 0", "App 1", "App 2", "App 3", "App 4",
        "App 5", "App 6", "App 7", "App 8", "App 9",

        "App 10", "App 11", "App 12", "App 13", "App 14",
        "App 15", "App 16", "App 17", "App 18", "App 19",
            
        "App 20", "App 21", "App 22", "App 23", "App 24",
        "App 25", "App 26", "App 27", "App 28", "App 29",
            
        "App 30", "App 31", "App 32", "App 33", "App 34",
        "App 35", "App 36", "App 37", "App 38", "App 39",
    ]
    
    # TODO: make this get all entries at the same time
    def get(self) -> list[App]:
        homed = Path.home()
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
            a_temp: App = App(p)
            if (not a_temp.is_hidden):
                apps.append(a_temp)
        
        return apps

    def __init__(self) -> None:
        self.apps = self.get()
        pass
