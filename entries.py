import os
from public import *

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

