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

        p_cmd = p_cmd.replace("%f", "")
        p_cmd = p_cmd.replace("%F", "")
        p_cmd = p_cmd.replace("%u", "")
        p_cmd = p_cmd.replace("%U", "")
        p_cmd = p_cmd.replace("%i", "")
        # keep this one at last to not mess up the others
        p_cmd = p_cmd.replace("%", "")

        return p_cmd
    

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
    w_data: Win_data
    paths: list[str]
    # all visible apps
    apps: list[App]
    # filtered apps
    # covered by Win_data
    #filtered_apps: list[App]

    
    # TODO: put some multithreading on this function
    def get(self,
    ) -> list[App]:
        '''
        homed: str = f"{Path.home()}"
        paths: list[str] = [
            "/usr/share/applications/",
            "/usr/local/share/applications/",
            f"{homed}/.local/share/applications/",
        ]
        '''
        #paths: list[str] = PATHS


        files: list = []; 
        for d in self.paths:
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

    # returns a new list of apps based that match their name with text
    def filter(self,
        text: str
    ) -> list[App]:
        if (text == ""):
            return self.apps

        f_entries: list[App] = []
        for app in self.apps:
            # set both to uppercase so that the search isn't case sensitive
            if (text.upper() in app.name.upper()):
                f_entries.append(app)
        return f_entries

    def __init__(self,
        data: Win_data,
        paths: list[str]
    ) -> None:
        self.w_data = data
        self.paths = paths

        self.apps = self.get()
        # handled by the window in .init_objects
        #self.w_data.set_entries(self.apps)
