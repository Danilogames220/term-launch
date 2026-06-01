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
    
    # curses enter doesnt work for me idk why
    "confirm": 10, #curses.KEY_ENTER,
   
    "switch-mode": 0, # ctrl + space
    
    "navigation": {
        "down": 67,
        "up": 67
    },

    "navigation-global": {
        "down": 67,
        "up": 67
    }
}

