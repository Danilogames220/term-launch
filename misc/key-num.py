# puts to the screen each ascii keycodes
# mostly used for ctrl+key codes
import curses

def main(win: curses.window) -> None:
    curses.set_escdelay(1)
    curses.curs_set(0)
    
    win.addstr(0, 0, "Curses keypress check", curses.A_BOLD)
    win.addstr(1, 0, "Press 'q'(113) or ctrl-c to exit", curses.A_ITALIC)
    
    while True:
        buf: int = win.getch()

        if (buf == ord('q')):
            exit(0)

        win.addstr(3, 0, f"key pressed: '{chr(buf)}'  ")
        win.addstr(4, 0, f"code: {buf}  ", curses.A_ITALIC)

curses.wrapper(main)
