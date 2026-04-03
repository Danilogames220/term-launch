from pathlib import Path
import curses

# command used for lauching apps
launch_command = "thing asdfasdf"
def launch(app):
    pass

# all dirs that have the application/ dir
# echo $xdg_data_dirs
homed = Path.home()
paths = [
    "/usr/share/applications/",
    "/usr/local/share/applications/",
    f"{homed}/.local/share/applications/",
]

# keys must be integers
keybinds = {
    "quit": 27, # escape
    
    "confirm": curses.KEY_ENTER,
   
    "switch-mode": 0 # ctrl + space

}

