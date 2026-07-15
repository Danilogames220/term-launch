import os
from public import *

# Holds data of each app
class App:
    name: str;
    path: str;
    raw_cmd: str;

    ex_cmd: str = "";
    is_hidden: bool = False
    is_terminal: bool = False
    
    def parse_cmd(self, 
        cmd: str
    ) -> str:
        p_cmd: str = cmd

        p_cmd = p_cmd.replace("%f", "")
        p_cmd = p_cmd.replace("%F", "")
        p_cmd = p_cmd.replace("%u", os.getcwd())
        p_cmd = p_cmd.replace("%U", "")
        p_cmd = p_cmd.replace("%i", "")
        p_cmd = p_cmd.replace("%", "") # keep this one at last to not mess up the others

        return p_cmd
    

    def __init__(self, path: str):
        self.path = path
        self.name = ""
        
        with open(path) as f:
            def check(l: str, arg: str) -> bool:
                return (l.find(arg) != -1)

            for line in f:
                # find app name
                if (check(line, "Name=")) and (len(self.name) == 0):
                    self.name = line.split("Name=")[1]
                    #self.name = line[line.find("Name="):]
                # find app launch command
                if (check(line, "Exec=")) and (self.ex_cmd == ""):
                    self.ex_cmd = line.split("Exec=")[1]

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
    
    def get(self) -> list[App]:
        files: list = []; 
        for d in self.paths:
            try:
                for f in os.listdir(d):
                    files.append(d + f)
            except:
                continue
    
        apps: list[App] = []
    
        for p in files:
            # check if it's a .desktop file
            ext: str = "desktop"
            if not (p[len(p) - len(ext):] == ext):
                    continue
            
            # check if it's a hidden entry
            a_temp: App = App(p)
            if (a_temp.is_hidden):
                continue

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

