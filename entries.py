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
        self.name = ""
        
        # TODO: move this to parse_file
        with open(path) as f:
            for line in f:
                # find app name
                if (line.find("Name=") != -1) and (len(self.name) == 0):
                    self.name = line.split("Name=")[1]
                    #self.name = line[line.find("Name="):]
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
