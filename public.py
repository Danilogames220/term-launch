from enum import Enum
import copy


class vec2:
    x: int = 0
    y: int = 0
    
    def __init__(self: vec2, X: int, Y: int):
        self.x = X
        self.y = Y
    
    def copy(self: vec2) -> vec2:
        return copy.deepcopy(self)
    #def __init__(self: vec2, v: vec2):
    #    self.x = v.x
    #    self.y = v.y


class modes(Enum):
    SEARCH = 0
    NAV = 1

# Holds data of each entry
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


