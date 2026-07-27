# Term-Launch
Application launcher via command-line made only with Python3 using the Curses library.

## Features:
- Minimalistic interface;
- No external libraries needed.
- Supports vim / vi like navigation;

## Compiling / intalling:
The only depedency needed for compiling (aside python) is [PyInstaller](https://pyinstaller.org/en/stable/) that is used for building the project

You can compile the code by running the following command: 
```
pyinstaller main.py -n tlaunch --onefile
```
or using the Makefile to compile and install the program
```
make install
```
### Uninstalling
To uninstall the program, you can just remove the desktop entry and the executable or also use the makefile
```
make uninstall
```

## How to use:
Find the application you want to run in the list or search for the app you want to launch using the search mode, move using the up or down arrow or j/k keys in the navigatation mode.
Currently the launcher only has 2 difrent modes, you can alternate between them using the change mode keybind. They are:
- **Search**(default): Used for applying a filter to the app list.
- **Navigation**: Used for moving between the app list. 

## Keybinds:

### All
- **Select:** Enter
- **Exit:** Escape
- **Change mode:** Ctrl + o

- **Move one app down**: Down-Arrow
- **Move one app up**: Up-Arrow

- **Move window down:** Shift + Down-Arrow
- **Move window up:** Shift + Up-Arrow

### Navigation mode

#### Move app selection
- **Move one app down**: j / Down-Arrow
- **Move one app up**: k / Up-Arrow

#### Move window
- **Down:** Shift + j / Shift + Down-Arrow
- **Up:** Shift + k / Shift + Up-Arrow

#### Misc
- **Select:** Enter
- **Exit:** Escape
- **Change mode:** Ctrl + o

### Search mode
- **Select:** Enter
- **Exit:** Escape
- **Change mode:** Ctrl + o
